# PXD017046：活化 Jurkat 细胞的 NPGPx 免疫沉淀

## 已核实并修正

- [PRIDE 提交记录](https://www.ebi.ac.uk/pride/archive/projects/PXD017046)说明样本来自表达 NPGPx、经 anti-CD3/anti-CD28 共刺激的 Jurkat 细胞；采用 NPGPx 抗体免疫沉淀，非还原 SDS-PAGE 后切取蛋白条带，并实际进行 Trypsin 胶内消化。已补充 `immunoprecipitation` 富集过程。
- 5 个归档 RAW 均已读取文件头：内部原始名称为 `2016-0517_Gpx7-1` 至 `Gpx7-5`，与 5 份作者 Mascot CSV 中的输入 MGF 对应。RAW 确认 Orbitrap Elite、DDA、CID 35 NCE、离子阱 MS2 和 350–1600 m/z 的 MS1 范围。
- 五份 CSV 均支持 10 ppm 前体容差、0.6 Da 碎片容差和现有七项可变修饰。Dimethyl、GlyGly、LeuArgGlyGly 是搜索的可变修饰，不能据此将样本解释为化学同位素标记实验。Phospho 的 S/T 位点格式改为 `S,T`。
- 原材料来自培养细胞，组织字段改为 `not applicable`。Jurkat 的 [Cellosaurus 记录 CVCL_0065](https://www.cellosaurus.org/CVCL_0065)支持原始供者为 14 岁男性；年龄按 human 1.1 模板记录为 `14Y`，不代表实验时细胞培养的持续时间。该记录的 population 值为 `Caucasian`，未直接提供旧稿使用的 `European ancestry` 分类，祖源字段暂缺。
- 提交记录与 CSV 只说明搜索允许 Carbamidomethyl C，未说明制备使用 IAA，已清除旧稿的 IAA 试剂断言。

## 尚待核实

- 1–5 是作者的编号文件，尚无逐条带分子量、独立免疫沉淀批次及培养重复的对应表。文件编号不能单独证明馏分编号，因此馏分和生物学重复均记为 `not available`。
- 五个编号是否均来自同一次免疫沉淀及同一份起始裂解物仍需补证。来源名称暂保留逐 RAW 的标识，避免将五份未知制备合并为一个来源；这些临时标识不代表已确认五个独立生物学样本。

结构检查与来源核对用于确认已补齐的字段；生物学重复和馏分必填项仍缺失，因此保留在 `sandbox/`。
