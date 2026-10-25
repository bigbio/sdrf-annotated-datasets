# PXD000600：旧稿存在关键错误，暂不采用

来源：[PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD000600)、[论文 PMID 24396086](https://doi.org/10.1074/mcp.M113.030916)及归档 [Eichelbaum.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2014/03/PXD000600/Eichelbaum.zip)。

## 核对结果

- 当前归档有 691 个 RAW，旧稿只列 13 个；这 13 个文件均实际存在，但不能代表完整项目。
- 已通过 HTTP Range 从作者 ZIP 提取 `parameters.txt`、`summary.txt` 和 `tables.pdf`。其中 `tables.pdf` 是 MaxQuant 输出字段说明，不是实验样本映射表。
- `summary.txt` 中这 13 个 RAW 的 `Multiplicity` 均为 2，`Labels0` 为空、`Labels1` 为 `Arg10;Lys8`，且参数文件关闭 label-free 定量。旧稿的 label-free 解释不成立；轻、重信号与具体生物样本/实验组的关系还需补齐。
- 逐一读取 13 个 RAW 文件头：`100706_KS1531_R15-5_1` 至 `_12` 来自 **LTQ Orbitrap XL**，`101029_KS_R16_1_1` 来自 **LTQ Orbitrap Velos**；全部方法均为 **CID**。旧稿统一的 Velos 和 HCD 注释错误，且 Velos 使用了不匹配的本体编号。
- 限量读取作者 `evidence.txt` 后，已直接确认 `_R15-5_5/6/8` 对应实验 `R15_5` 的馏分 5/6/8，`_R16_1_1` 对应实验 `R16_1` 的馏分 27。它们不能按旧稿的文件排序拆成对照、不同处理时点和技术重复。
- 作者项目的核心时间序列是 RAW 264.7 细胞的 SILAC/AHA 研究；旧稿的 0/1/4/24 小时与逐 RAW 的关系没有来源支持。论文还涉及多种样本制备，因此不能把同一套酶、分级方法或修饰无差别填入全部文件。

## 继续工作所需证据

需要恢复 `R15_5`、`R16_1` 等实验编号与样本材料、处理、时间、标签交换及生物学重复的完整对应，再按 SILAC 设计重建行。论文有样本整体设计，现有归档元数据尚不能把这些设计准确落实到旧稿的 13 个 RAW。

本次只记录可复核的错误和证据，旧 SDRF 暂保留为待重建草稿，**不得用于正式分析或移入 `datasets/`**。核对日期：2026-09-27。
