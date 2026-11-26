# PXD008510：合样信息已修正，逐运行重复关系待确认

来源：[PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD008510)、[论文 PMID 29288089](https://pmc.ncbi.nlm.nih.gov/articles/PMC5803406/)，以及全部五个 RAW 的文件头。

## 已确认

- 作者说明有两份独立生物学合样，每份包含 15 对唾液腺，混合第五龄若虫和成虫材料。已补充 `pooled sample=pooled` 及混合发育阶段说明；不把混合材料统一标成成年个体。
- 档案共有五个 RAW：`Tdim-y1-2.raw`、`Tdim-y1-3.raw`、`Tdim-y2.raw`、`Tdim-y2-2.raw`、`Tdim-y2-3.raw`。全部属于本项目，未补造不存在于清单的第六个运行。
- 文件头保留作者原始运行名 `Y1-2`、`Y1-3`、`Y2`、`Y2-2`、`Y2-3`，已写入 `comment[author acquisition identifier]`。
- 五个文件头均为 Orbitrap Elite、CID 35 NCE、离子阱 MS2、300–1800 m/z。实际方法记录 Top 20，论文写 Top 15；未把正文的 Top 15 套入文件级参数。
- 论文明确实际 Trypsin 消化、DTT / IAA 处理；搜索为固定 Carbamidomethyl C、可变 Oxidation M，容差 10 ppm / 0.5 Da。

## 尚待补齐

当前取得的公开资料没有明确列出两个生物学合样与五个 RAW 的对应表。`Y1/Y2` 和末尾编号与原草稿分组相容，但仅凭文件名不足以确定样本身份及技术重复顺序。因此生物学重复和技术重复暂记 `not available`。源名暂以 RAW 标识占位，不表示存在五个独立生物学样本。

档案中的合并 pdResult / MSF 约为 1.8 / 3.3 GB；本轮仅读取 pdResult 前 2 MiB，未取得可核验的样本设计表，也未下载这些完整大文件。仍需作者的合样—运行映射才能正式定稿。必填重复信息缺失，继续保留在 `sandbox/`。

核对日期：2026-09-27。
