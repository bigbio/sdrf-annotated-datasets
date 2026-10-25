# PXD005253：MCF-7 的 FOXA1 RIME

## 本轮修正

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD005253)中的 5 个 MSF 均完成归档 SHA1 校验，`FileInfos` 与对应的 5 个 RAW 一致。
- 所有 MSF 均采用可变 Oxidation（M）和 Deamidated（N/Q），没有配置固定 Carbamidomethyl。已撤回旧草稿的固定修饰，补全可变修饰、10 ppm 前体容差和 0.8 Da 碎片容差。
- MSF 实际设置为 Trypsin、允许 1 个漏切位点；[论文](https://doi.org/10.1016/j.celrep.2016.11.028)及提交说明写的是最多 2 个漏切位点，二者存在差异，不能混为同一搜索设置。
- 5 个 RAW 文件头均支持 LTQ Orbitrap Velos 和 CID。`PR090`、`PR099` 的嵌入样本标签明确含 FOXA1/MCF7；`PR164` 的两份 RAW 分别明确为 FOXA1 和 IgG。已区分研究样本与 IgG 阴性对照，并用文件标签替换没有来源含义的 `sample_1` 等名称。
- `PR131_KAY_171111_Untreated.raw` 的嵌入标签仅明确 MCF7/Untreated，没有明确免疫沉淀靶标或对照角色；新增样本角色及相应实验因子保留为 `not available`。
- 正文确认 DMEM 培养和 STR 鉴定；[Cellosaurus CVCL_0031](https://www.cellosaurus.org/CVCL_0031)支持既有细胞系来源信息。
- 来源交叉检查对 PR131 报告 `disease_on_control_runs`：它由文件名中的 `Untreated` 推断对照必须没有乳腺癌属性。RAW 标签明确为 MCF7，Cellosaurus 确认该细胞系的肿瘤来源，因此保留 `breast cancer`；未处理状态本身不能改变细胞系的来源疾病。该启发式告警已记录，未修改检查规则。

## 保留在 sandbox 的原因

- 论文称进行了 5 次 FOXA1 RIME，但归档的 5 个 RAW 中包含 IgG 对照。补充表 S1 只有汇总的蛋白/肽信息，没有提供逐实验文件映射。
- 旧稿生物学重复编号 1 至 5 尚未证实。当前来源名称只是可追溯的文件标签，不能据此把全部 5 行当作 5 个 FOXA1 生物学重复。
- 仍需明确 PR131 的靶标、研究样本与对照的配对关系，以及论文所述重复与归档文件的覆盖关系。

本轮结构及解析检查通过；上述证据缺口仍阻止进入 `datasets/`。
