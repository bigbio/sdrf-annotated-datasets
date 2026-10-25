# PXD013060：神经祖细胞条件培养基分泌组

## 已核实并修正

- [PRIDE 提交记录](https://www.ebi.ac.uk/pride/archive/projects/PXD013060)及[原论文](https://doi.org/10.1073/pnas.1818348116)说明质谱检测的是 iPSC 衍生神经祖细胞的条件培养基。旧草稿的 `material type=cell line` 不能描述送检材料，改为 `not available`；当前枚举没有条件培养基。细胞来源保留在 cell type、cell line 等列中。
- 归档的 5 个 RAW 均读取了文件头。以下原始细胞系和代次来自 RAW 内部样本名称，而非依据文件顺序推测。

| 归档 RAW | 内部细胞系 | 代次 | 内部标签中的处理 |
| --- | --- | --- | --- |
| OTF17-3347_Crocker_Line3PPMS_P9.raw | 148-2 | 9 | 无 rapa 标记 |
| OTF17-3352_Crocker_Line3rapa.raw | 148-2 | 9 | rapa |
| OTF17-3357_Crocker_Line3.1control.raw | 147-3 | 6 | 无 rapa 标记 |
| OTF17-3362_Crocker_Line1.raw | 100-4 | 19 | 无 rapa 标记 |
| OTF17-3367_Crocker_Line1rapa.raw | 100-4 | 18 | rapa |

- 项目说明对照、PPMS 和雷帕霉素处理的 PPMS 条件；归档文件名也明确标出 PPMS、control 和 rapa。保留这些条件，细胞系编号采用上表。去掉原先由文件标签生成但没有供者对应证据的 individual 值。
- 样本处理记录明确为 Q Exactive Plus，并给出 HCD、28 NCE、MS1 300–1700 m/z、MS2 200–2000 m/z 和 2–6 电荷选择。RAW 文件头也支持 HCD。项目顶层的普通 Q Exactive 仪器标签不能覆盖更详细的方法和文件证据。
- 搜索设置支持固定 Carbamidomethyl C、可变 Oxidation M、10 ppm 前体和 0.02 Da 碎片容差。Carbamidomethyl 搜索修饰不能证明实际使用 IAA，已将烷基化试剂改为缺失。

## 尚待核实

- 论文称不同细胞系保持一致代次，但 RAW 文件头显示 P9、P9、P6、P19、P18。当前记录实际 RAW 中的值；该冲突尚未解决，不能宣称消除了代次效应。
- 论文中的四个技术重复、三组独立培养属于 OPC 功能实验，不能直接套到这 5 个质谱文件。独立培养、合样及供者关系尚未核实，已清除旧的生物学重复 1/2 编号；合样状态为 `not available`。
- 制备记录未说明实际消化酶，Mascot 的 stricttrypsin 仅为搜索设置。`cleavage agent details` 改为 `not available`，不以搜索酶替代实际制备证据。
- 细胞系补充表 S2 尚未取得：出版社补充 PDF 返回 403，Europe PMC 补充 ZIP 的传输中断。未以未读取的补充表确认供者信息。

结构检查无错；当前解析器在生物学重复和实际消化酶两个必填项上报错。补齐这些科学证据前保留在 `sandbox/`。
