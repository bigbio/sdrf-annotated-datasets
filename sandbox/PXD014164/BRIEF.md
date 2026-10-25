# PXD014164：半重组 U7 snRNP 复合物

## 已核实的修正

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD014164)包含 5 个 RAW 和 5 个 Mascot XML。全部 XML 的文件对应关系与提交清单一致，下载结果通过归档 SHA1 校验。
- 5 个 RAW 文件头均为 Orbitrap Elite；各 XML 的 `_DISTILLER_INSTRUMENT_MODEL` 也为 `MS:1001910`。据此纠正项目页面及旧草稿中的 Q Exactive，碎裂方式为 HCD。
- XML 一致记录前体容差 30 ppm、碎片容差 0.1 Da、固定 Carbamidomethyl（C）和可变 Oxidation（M）。实际搜索采用 semiTrypsin、允许 1 个漏切位点；提交记录的样本制备明确使用 trypsin，消化酶字段据此保留。
- [原论文](https://doi.org/10.1093/nar/gkz1148)描述的是体外组装、亲和纯化的复合物，撤回 `material type=tissue`。模板没有准确描述这种材料的枚举值，暂记 `not available`。
- 当前可核实的制备记录未明确指定 IAA，撤回该试剂断言。搜索中的 Carbamidomethyl 不能单独证明使用 IAA。

## 保留在 sandbox 的原因

- 尚缺 `gel_C`、`gel_D` 以及三个溶液样本与具体图版条件、独立制备批次的逐文件对应表。旧稿的解释性来源名称和重复编号不能视为已核实。
- 实验含重组蛋白、合成 RNA 和小鼠核提取物；需要逐条件确认物种组成。数据库搜索限制为小鼠，不能证明所有重组组分都来自小鼠，也不能直接证明无提取物对照的物种。

本轮结构及解析检查通过，保留 `no_factor_value` 提示。样本条件、重复关系和混合来源补齐前不进入 `datasets/`。
