# PXD004135：肠液与肠源性碳酸钙有机基质

## 已核实的证据

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD004135)及[完整文件清单](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD004135/files/all)包含 5 个 RAW：`IF_2.raw`、`IF_3.raw`、`Matrix_1-2_150429225102.raw`、`Matrix_3-4.raw`、`Matrix_5-6.raw`。草稿覆盖全部 5 个文件。
- [Schauer 等，2016](https://doi.org/10.1038/srep34494)的图 2 明确报告 2 个肠液样本和 3 个严格纯化的碳酸钙基质样本。它们不是肠组织活检。
- 论文方法说明：严格纯化组的沉淀按鱼缸跨日期汇集；提取后的上清可进一步合并。3 个 `Matrix_*` 样本因此标记为 `pooled`。现有资料不能确定每个池的供体数量或贡献关系；文件名中的 `1-2` 等不得解释为两条鱼。
- 5 个提交的 mzIdentML 文件分别对应上述样本。导出路径包含 `Stringent` 和 `IF1 removed`，与本项目仅保留 `IF_2`、`IF_3` 的文件清单一致；不补造 `IF_1`。
- 各 mzIdentML 搜索设置一致：Carbamidomethyl（C）为固定修饰，Oxidation（M）为可变修饰；前体容差 10 ppm，碎片容差 0.4 Da。Trypsin 和 Orbitrap Velos Pro 由论文方法及提交者协议确认；PRIDE 的结构化仪器字段较宽泛。

## 保留在 sandbox 的原因

- `IF_2`、`IF_3` 的供体或混样构成尚不能逐样本确定，因此 `characteristics[pooled sample]` 保留 `not available`。
- 不把数值重复编号解释为单条鱼，也不把 3 个基质池默认当成来自互不重叠供体的生物学重复。
- 论文没有给出可用于逐样本标注的疾病诊断；`characteristics[disease]` 使用 `not available`。
- 当前 `material type` 枚举不能准确表达肠液和矿物相关有机基质，撤回原先的 `tissue`，使用 `not available`。现有解剖部位字段仍较粗，后续应保留并明确肠液与基质的区别。

以上仅补齐有来源依据的字段；解析通过不能替代供体和混样对应关系的核实。
