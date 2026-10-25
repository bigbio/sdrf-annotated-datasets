# PXD076440：斑马鱼视网膜 DDA/DIA-PASEF

## 已核实

- [PRIDE 提交记录](https://www.ebi.ac.uk/pride/archive/projects/PXD076440)和作者提交的 `SDRF.sdrf.tsv` 列出 16 条鱼，每条鱼的双眼视网膜合并后分别进行 DDA、DIA 分析，共 32 次运行。两个模式使用相同的样本名和作者的生物学重复编号。
- 通过读取两个 RAW 压缩包的 ZIP 目录，逐一确认全部 32 个 `.d` 目录。`DDA_PASEF_raw_data.zip` 包含 16 个 DDA 目录；名称看似单样本的 `20251120_SW1_BB2_1_31426.d.zip` 实际包含全部 16 个 DIA 目录。SDRF 的 `data file` 为内部目录名，`file uri` 指向对应压缩包。补回作者 SDRF 中 16 个 DDA 文件名漏写的 `.d` 后缀。
- 实际消化使用 Trypsin 和 Lys-C，已分列记录；Trypsin/P 是搜索设置。仪器为 timsTOF Pro 2。依提交记录将蛋白 N 端乙酰化改为可变修饰，并保留固定 Carbamidomethyl C、可变 Oxidation M。
- 10 ppm 前体和碎片容差仅用于明确报告这些参数的 DIA 分析；DDA 容差暂缺。双眼合样记录为 `pooled`，不代表混合不同动物。

## 尚待核实

- 作者 SDRF 将 WT1–WT8、SW1–SW8 全部标为成年、近视，但项目描述未解释 WT/SW 分组，也未给出疾病状态或处理条件的逐样本说明。草稿保留作者报告的 `myopia`，不可据文件名擅自把 WT 改为健康对照，也不可把全体近视视为已独立确认。分组说明补齐前保留在 `sandbox/`。
- 来源核对工具据 WT 文件名报告 `disease_on_control_runs`，这是需要核实的歧义；它同时报告缺少 Lys-C，但 SDRF 两个消化酶列已分别明示 Trypsin 和 Lys-C，该项为工具对重复列的识别问题。

当前主线解析器和仓库审查脚本通过，只有缺少实验因子列的提示。格式检查通过不等于上述分组歧义已解决。
