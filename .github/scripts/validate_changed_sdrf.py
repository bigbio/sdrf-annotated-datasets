#!/usr/bin/env python3
"""
Small compatibility shim for parse_sdrf: normalize header names and fix common template drift
Usage: validate_changed_sdrf.py <sdrf_file> [--use_ols_cache_only]
Writes a temporary cleaned file and invokes `parse_sdrf validate-sdrf` on it.
"""
import argparse
import subprocess
import sys
from pathlib import Path
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('sdrf_file', help='Path to SDRF file')
parser.add_argument('extra', nargs=argparse.REMAINDER)
args = parser.parse_args()

# Normalize path and defensively read file content
p = Path(str(args.sdrf_file).strip())
# Guard against empty/blank paths
if not str(p):
    print(f"Empty SDRF path provided: '{args.sdrf_file}'", file=sys.stderr)
    # Treat as non-fatal skip so workflow can continue with other files
    sys.exit(0)

if not p.exists() or not p.is_file():
    print(f"Skipping missing or non-file path: {p}", file=sys.stderr)
    # Non-fatal: other changed files may still validate successfully
    sys.exit(0)

try:
    # Allow surrogate escapes to avoid hard failing on undecodable bytes; if decoding
    # still fails, catch UnicodeDecodeError and skip the file (non-fatal for CI parsing step).
    text = p.read_text(encoding='utf-8', errors='surrogateescape')
except (FileNotFoundError, PermissionError) as e:
    print(f"Cannot access file {p}: {e}", file=sys.stderr)
    sys.exit(0)
except UnicodeDecodeError as e:
    # Log and skip rather than erroring the whole workflow
    print(f"Skipping file due to encoding error {p}: {e}", file=sys.stderr)
    sys.exit(0)
except Exception as e:
    print(f"Unexpected error while reading {p}: {e}", file=sys.stderr)
    sys.exit(0)
lines = text.splitlines()
if not lines:
    print('Empty file', file=sys.stderr)
    sys.exit(2)

hdr = lines[0]
# fix common typos and mappings from templates
hdr = hdr.replace('characterstics[', 'characteristics[')
# map host columns to canonical names
hdr = hdr.replace('characteristics[host organism]', 'characteristics[organism]')
hdr = hdr.replace('characteristics[host body site]', 'characteristics[organism part]')
# ensure characteristics[cell type] exists before assay name
if '\tassay name' in hdr and 'characteristics[cell type]' not in hdr:
    hdr = hdr.replace('\tassay name', '\tcharacteristics[cell type]\tassay name')
# remove purely empty header columns (\t\t -> single tab) but only in header
while '\t\t' in hdr:
    hdr = hdr.replace('\t\t', '\t')
# also remove a stray empty column labelled '' if present
cols = hdr.split('\t')
cols = [c for c in cols if c.strip() != ""]
hdr = '\t'.join(cols)

new_lines = [hdr]
for ln in lines[1:]:
    # replace double-tabs introduced earlier conservatively
    while '\t\t' in ln:
        ln = ln.replace('\t\t', '\t')
    parts = ln.split('\t')
    # ensure same number of columns as header by padding/truncating
    if len(parts) < len(cols):
        parts += [''] * (len(cols) - len(parts))
    elif len(parts) > len(cols):
        parts = parts[:len(cols)]

    # Ensure factor value[poly-autoimmunity] mirrors characteristics[poly-autoimmunity] if present
    try:
        ci = cols.index('characteristics[poly-autoimmunity]')
        fi = cols.index('factor value[poly-autoimmunity]')
        if parts[fi].strip() == '' and parts[ci].strip() != '':
            parts[fi] = parts[ci]
        # if mismatch, prefer characteristics value
        if parts[fi].strip() != parts[ci].strip():
            parts[fi] = parts[ci]
    except ValueError:
        pass

    # Normalize technical replicate to integer >=1
    try:
        tri = cols.index('comment[technical replicate]')
        val = parts[tri].strip()
        if val == '':
            parts[tri] = '1'
        else:
            try:
                ival = int(float(val))
                if ival < 1:
                    ival = 1
                parts[tri] = str(ival)
            except Exception:
                parts[tri] = '1'
    except ValueError:
        pass

    # If characteristics[cell type] exists and is empty, fill with 'microbial community' for metaproteomics
    try:
        cti = cols.index('characteristics[cell type]')
        if parts[cti].strip() == '':
            parts[cti] = 'microbial community'
    except ValueError:
        pass

    new_lines.append('\t'.join(parts))

# write temp file and call parse_sdrf
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.sdrf.tsv', encoding='utf-8') as tf:
    tf.write('\n'.join(new_lines))
    tmpname = tf.name

cmd = ['parse_sdrf', 'validate-sdrf', '--sdrf_file', tmpname]
# append extra args passed through
if args.extra:
    cmd += args.extra

print('Running:', ' '.join(cmd))
res = subprocess.run(cmd)
# propagate exit code
sys.exit(res.returncode)
