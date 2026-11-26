"""Exercise the release workflow with the same Bash flags as GitHub Actions."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest


WORKFLOW = (Path(__file__).resolve().parents[1] / ".github" / "workflows"
            / "validate-on-sdrf-pipelines-release.yml")


def validation_script():
    # Read this literal run block without adding a YAML dependency to the gate tests.
    step = next(part for part in WORKFLOW.read_text().split("\n      - ")
                if "\n        id: validate\n" in part)
    script = textwrap.dedent(step.split("\n        run: |\n", 1)[1])
    return script.replace("${{ steps.ver.outputs.version }}", "0.1.6")


def run_validation(tmp_path, tracked, failures=None):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for name in tracked:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test SDRF\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    # An untracked SDRF must not be included in a release check.
    (tmp_path / "datasets" / "untracked.sdrf.tsv").write_text("untracked\n")

    (tmp_path / "results.json").write_text(json.dumps(failures or {}))
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    timeout = bin_dir / "timeout"
    timeout.write_text(f"#!{sys.executable}\n" + textwrap.dedent("""\
        import json
        from pathlib import Path
        import sys

        with open("calls.jsonl", "a") as calls:
            calls.write(json.dumps(sys.argv[1:]) + "\\n")
        path = sys.argv[sys.argv.index("--sdrf_file") + 1]
        code, output = json.loads(Path("results.json").read_text()).get(path, [0, "OK\\n"])
        sys.stderr.write(output)
        sys.exit(code)
        """))
    timeout.chmod(0o755)
    script = tmp_path / "validate.sh"
    script.write_text(validation_script())
    output = tmp_path / "github-output"
    output.touch()
    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", str(script)],
        cwd=tmp_path,
        env={**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
             "GITHUB_OUTPUT": str(output)},
        capture_output=True,
        text=True,
        timeout=30,
    )
    calls = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    outputs = dict(line.split("=", 1) for line in output.read_text().splitlines())
    return result, calls, outputs


@pytest.mark.parametrize("exit_code,diagnostic", [
    (1, "Detailed context\nERROR: invalid annotation\n"),
    (2, "Validation failed without a standard error prefix\n"),
    (124, ""),
])
def test_collects_failure_and_continues_under_runner_errexit(tmp_path, exit_code, diagnostic):
    failed = "datasets/PXD000001/PXD000001.sdrf.tsv"
    passed = "datasets/PXD000002/PXD000002.sdrf.tsv"
    result, calls, outputs = run_validation(
        tmp_path, [failed, passed], {failed: [exit_code, diagnostic]},
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert [call[call.index("--sdrf_file") + 1] for call in calls] == [failed, passed]
    assert outputs == {"fail_count": "1", "total": "2"}
    assert f"FAIL (exit {exit_code}): {failed}" in result.stdout
    assert f"Validating: {passed}" in result.stdout
    report = (tmp_path / ".ci-artifacts" / "failures.md").read_text()
    assert failed in report
    assert passed not in report
    assert f"Exit code: {exit_code}" in report
    if diagnostic:
        assert diagnostic.splitlines()[-1] in report
        assert diagnostic.splitlines()[-1] in result.stdout
    log = tmp_path / ".ci-artifacts" / "logs" / f"{failed}.log"
    assert log.read_text() == diagnostic


def test_validates_only_tracked_canonical_files_with_matching_templates(tmp_path):
    affinity = "datasets/PAD000001/PAD000001.sdrf.tsv"
    ms = "datasets/PXD000001/PXD000001.sdrf.tsv"
    result, calls, outputs = run_validation(tmp_path, [
        ms, affinity, "sandbox/PXD000002/PXD000002.sdrf.tsv", "datasets/PXD000001/README.md",
    ])

    assert result.returncode == 0, result.stdout + result.stderr
    assert calls == [
        ["300", "parse_sdrf", "validate-sdrf", "--sdrf_file", affinity,
         "--use_ols_cache_only", "-t", "affinity-proteomics"],
        ["300", "parse_sdrf", "validate-sdrf", "--sdrf_file", ms, "--use_ols_cache_only"],
    ]
    assert outputs == {"fail_count": "0", "total": "2"}
    assert (tmp_path / ".ci-artifacts" / "failures.md").read_text() == ""
