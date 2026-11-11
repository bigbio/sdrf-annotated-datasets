# PXD005428：CD99 蛋白水解研究

## 本轮已核实并修正

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD005428)包含 5 个 RAW。全部文件头均记录 `Q Exactive Plus`，并包含数据依赖采集设置，已纠正原先较宽泛的仪器名称。
- 提交协议明确使用共转染 myc/FLAG-tagged CD99 和未标记 meprin beta 的 HeLa 细胞，并进行抗 FLAG 免疫沉淀。补充转染和富集字段，来源名称保留构建体背景。
- [Cellosaurus CVCL_0030](https://www.cellosaurus.org/CVCL_0030)确认 HeLa 来源于子宫颈；`organism part` 由 `cell culture` 改为 `uterine cervix`。原有年龄、性别及细胞系字段与参考记录一致。
- 当前可核实的提交协议没有明确给出培养基、还原和烷基化试剂，相关字段改为 `not available`。搜索中的 Carbamidomethyl 不能单独证明使用了 IAA。

## 保留在 sandbox 的原因

- `CD_99_1` 至 `CD_99_4` 的独立 Sequest 结果均为无酶特异性搜索，采用固定 Carbamidomethyl（C）、固定 Dimethyl（K）及可变 Dimethyl（肽 N 端）。合并的 Mascot 复核结果仅覆盖同一组 4 个 RAW，其修饰设置不同；不能把它当作第 5 次进样的搜索结果。
- `CD_99_4_6uL_INC.raw` 存在于提交清单，但不在合并 MSF 的文件对应表中。此行的具体搜索参数仍缺逐文件证据，不能声明已经全部核实。
- 草稿原有的 Trypsin 尚未从本项目的完整样本制备记录中确认。无酶特异性搜索不等于样品没有使用消化酶；目前既不据此改成无酶消化，也不把该旧字段视作已经验证。
- 凝胶条带编号、各 RAW 和重复进样的对应关系仍需原论文的补充图及实验记录核对。

原论文：[Bedau 等，2017](https://doi.org/10.1096/fj.201601113R)。本文件记录已修正项和剩余证据缺口，不能替代后续逐样本审核。
