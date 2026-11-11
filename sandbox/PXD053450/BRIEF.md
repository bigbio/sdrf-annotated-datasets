# PXD053450：心包液与心肌载体实验

已将证据闭合的 1,120 行患者心包液子集移入
`datasets/PXD053450/PXD053450-pericardial-fluid.sdrf.tsv`。本文件保留完整
155-RAW 草稿；参考、心肌载体/单独测定及比例优化行仍在 sandbox，因其混样、
馏分或重复关系未闭合。

本项目仍为部分修复的草稿。已重建 80 名患者的样本—TMT 通道—RAW 对应；优化实验和心肌单独测定的剩余缺口见下文。

## 来源及实验设计

- [PRIDE 提交记录](https://www.ebi.ac.uk/pride/archive/projects/PXD053450)、[原论文](https://doi.org/10.1016/j.mcpro.2024.100812)及[补充工作簿](https://ars.els-cdn.com/content/image/1-s2.0-S1535947624001026-mmc1.xlsx)。工作簿 SHA256 与 mzTab 蛋白定量段的逐值核对记录保存在本次本地核验记录中。
- 归档共有 155 个 RAW：126 个患者实验 RAW（有载体、无载体各 9 套 TMT × 7 个馏分），21 个载体比例优化 RAW，以及 8 个心肌单独测定 RAW。
- 患者样本是心包液。心肌仅用作载体或单独鉴定；该项目借鉴单细胞蛋白质组技术，不是单细胞实验。已删除单细胞模板、细胞编号、每孔细胞数及相关仪器字段。
- 患者分为 control、HF、DM、HF+DM，各 20 人。control 同样来自心脏手术患者，只表示无 HF、无 DM，不能写成健康。两列 `characteristics[disease]` 分别记录 HF 和 DM，合并疾病组同时保留两项；对照的其他疾病未提供，使用 `not available`。
- 患者通道为 127N–131N，126 为全部患者心包液的混合参考；有载体实验的 131C 为心肌载体。无载体实验不建立 131C 样本行。

## 患者与通道映射的核验方法

作者没有直接提供患者编号—TMT 通道表。以下映射由同一份原始结果在两个公开文件中的逐值身份对应恢复：

1. 补充表 S3、S4 的第 180–259 列为 80 个患者的原始 abundance ratios；第 4、5 行分别明确给出患者编号和临床组。
2. `Exp_Saet_9_WithCarrier_H.mzTab`、`Exp_Saet_9_NoCarrier_H.mzTab` 的 `protein_abundance_study_variable` 是以 126 通道为 100 的数值，除以 100 后与上述比例比较。
3. 有载体表按 UniProt accession 对齐 1398 个蛋白，每名患者至少 1008 个可比较值完全一致；无载体表对齐 265 个蛋白，每名患者至少 208 个值一致。全部匹配的最大绝对浮点差小于 `4e-15`，每列只对应一个候选通道。没有用相关性或疾病相关蛋白推断临床组。
4. 补充表部分 `0.01` 对应 mzTab 的缺失值；另有 4 个 `0.01` 对应低于 `0.01` 的 mzTab 比例。这些位置已逐项记录并排除出身份匹配证据，未据此推断作者未说明的插补流程。其余可比较值均须一致。
5. mzTab 的 `study_variable → assay → quantification_reagent/ms_run_ref` 给出通道和 7 个 RAW。两套结果独立核对后，80 人的 TMT 套号、通道和临床组全部一致；126 个 RAW 均在归档清单中。

下表编号来自作者补充表，两种载体条件共用。HF 为心力衰竭，DM 为 2 型糖尿病。

| TMT set | 127N | 127C | 128N | 128C | 129N | 129C | 130N | 130C | 131N |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 (control) | 2 (control) | 21 (HF) | 3 (control) | 41 (DM) | 42 (DM) | 22 (HF) | 61 (HF+DM) | 43 (DM) |
| 2 | 44 (DM) | 4 (control) | 5 (control) | 45 (DM) | 23 (HF) | 62 (HF+DM) | 6 (control) | 7 (control) | 46 (DM) |
| 3 | 24 (HF) | 63 (HF+DM) | 64 (HF+DM) | 25 (HF) | 65 (HF+DM) | 8 (control) | 9 (control) | 26 (HF) | 27 (HF) |
| 4 | 10 (control) | 47 (DM) | 28 (HF) | 11 (control) | 66 (HF+DM) | 67 (HF+DM) | 68 (HF+DM) | 69 (HF+DM) | 29 (HF) |
| 5 | 30 (HF) | 70 (HF+DM) | 71 (HF+DM) | 72 (HF+DM) | 31 (HF) | 32 (HF) | 48 (DM) | 12 (control) | 33 (HF) |
| 6 | 73 (HF+DM) | 13 (control) | 74 (HF+DM) | 75 (HF+DM) | 49 (DM) | 14 (control) | 50 (DM) | 76 (HF+DM) | 51 (DM) |
| 7 | 77 (HF+DM) | 15 (control) | 16 (control) | 52 (DM) | 34 (HF) | 53 (DM) | 35 (HF) | 17 (control) | 78 (HF+DM) |
| 8 | 18 (control) | 54 (DM) | 19 (control) | 79 (HF+DM) | 20 (control) | 55 (DM) | 36 (HF) | 37 (HF) | 80 (HF+DM) |
| 9 | 38 (HF) | 39 (HF) | 56 (DM) | 57 (DM) | 58 (DM) | 59 (DM) | 40 (HF) | 60 (DM) | 未对应 |

第 9 套 131N 没有对应补充表中的患者。草稿不为此创建第 81 名患者，也未据此断言该通道为空。患者生物学重复编号沿用作者的 1–80，跨有/无载体实验保持一致。参考样本的生物学重复标为 `pooled`。馏分编号保留 RAW 板位的数字 4–10；mzTab 的 F30 等实验组标识记录在 `sample preparation batch` 中，以区分各套混合样本。

## 技术参数修正

- 实际心包液消化为 Trypsin，心肌为 Lys-C 后接 Trypsin；均有 IAA 处理证据。仪器为 Orbitrap Exploris 480，DDA、HCD 35 NCE、前体 8 ppm、碎片 0.05 Da。
- 11 重 TMT 使用 TMT6plex 的修饰化学名称（UNIMOD:737），K 和肽 N 端为固定修饰。标签通道数与该化学名称并不矛盾。
- 固定 Carbamidomethyl C、可变 Oxidation M 和 Deamidated N/Q 由提交结果支持。患者 mzTab 不含论文概括描述的 Carbamyl，未强加到患者行；心肌 mzTab 包含 Carbamyl。优化结果还含 Acetyl 和未充分解释的 CHEMMOD，位点信息待核实。

## 保留在草稿区的原因

- 当前 1338 行覆盖全部 155 个 RAW，其中 1120 行为 80 名患者的双条件、7 馏分测定，126 行为参考，63 行为心肌载体。
- 21 个比例优化 RAW 暂以每次运行一行记录，标签和生物学重复未知；这些行不是完整的多重标记注释。尚需确认各比例及纯载体/纯心包液对照的实际占用通道，并补齐馏分信息。
- 8 个心肌单独测定 RAW 与论文提到的 4 名组织供者之间，合样、馏分和重复关系不清。载体供者及合样组成同样未说明；不把每个 RAW 当作新供者或独立生物学重复。
- 对未知的生物学重复、馏分及技术重复使用 `not available`。这些值会触发当前模板的必填项错误；保留错误以体现真实证据缺口，不填入任意数字换取校验通过。

文件已经过结构检查；必填项仍不完整，不能移入 `datasets/`。

本地本体缓存另对 `study sample` 报未收录；在线 OLS 已确认其为 PRIDE:0001013。IAA 已按现行标签 `Iodoacetamide (IAA)`、PRIDE:0000599 记录。本体缓存提示与上述真实的必填项缺失分别保留，未通过忽略规则隐藏。
