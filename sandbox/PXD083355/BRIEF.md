# PXD083355：NRL5 邻近标记与低水势处理

## 草稿依据

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD083355)及作者的 [ExperimentalDesign.csv](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/09/PXD083355/ExperimentalDesign.csv)支持 33 行样本与 RAW 的逐一对应；表中的 33 个文件完整覆盖归档的 33 个 `.d.zip`。
- 保留作者的样本名称、三种构建体及 control / low water potential（−0.7 MPa）条件。作者表中的各构建体有 6 个 control 标签、5 个 stress 标签；`R` 后缀按组编号，不能当作跨条件配对键。
- 生物材料为拟南芥幼苗。生长记录支持连续光照及 22 °C；项目记录支持 timsTOF HT、实验样本 DIA-PASEF 和无标记定量。DDA 是另行建库步骤，没有据此新增 DDA 样本行。
- 搜索方法支持固定 Carbamidomethyl（C），以及可变 Oxidation（M）、Acetyl（Protein N-term）和 Acetyl（K）。这些列记录识别参数。
- 一条作者来源记录对应一个已提交的 RAW，技术重复暂按该来源的单次记录编号为 1；不能据此推断不同 `R` 来源之间的重复类型。

## 阻断正式收录的缺口

- 作者表未说明 `R` 是独立生物学重复还是技术重复，故 `characteristics[biological replicate]` 保留 `not available`。
- Trypsin / LysC 仅出现在谱图库搜索设置中，提交的制备方法未说明实际消化步骤。因此 `comment[cleavage agent details]` 保留 `not available`。
- 来源核对工具将上述搜索设置识别成实际消化方法，报 `cleavage_agent_contradicted` 和 `cleavage_agent_incomplete`；这两个提示没有提供独立的制备证据，未据此补填消化酶。
- 未取得分段设计说明，`comment[fraction identifier]` 保留 `not available`。不能把文件名中的进样序号直接解释成分段编号。
- 提交记录称先混合多个独立转基因株系的种子，但这不等于每个质谱样本的混样方式已确认；未据此添加样本混池字段。

这些未知值使草稿不满足当前模板的必填值要求。仅保存在 `sandbox/`，不能作为验证通过的正式注释。

## 本轮检查

- 行宽、重复表头保留、样本坐标及 33/33 RAW 覆盖检查通过；解析器报告上述三个必填字段的未知值。
- 幼苗阶段使用 EFO 导入的 PO:0007131 标准标签 `seedling development stage`，植物模板已接受该术语。
- DIA 使用 PRIDE:0000450。2026-09-27 的 OLS 实时层级包含 PRIDE:0000659，但缓存模式校验仍提示其不属于该父项；该缓存警告保留，没有更改本体缓存或校验规则。
