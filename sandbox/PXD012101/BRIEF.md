# PXD012101：人脑 LCM 微量蛋白质组，非单细胞实验

## 来源与完整性

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD012101)、[论文 PMID 30768908](https://doi.org/10.1021/acs.jproteome.8b00981)、Supplementary Table S1/S2，以及归档 `txt.zip` 中的 MaxQuant `summary.txt` 和 `parameters.txt`。
- 全部 76 个 RAW 均与 `summary.txt` 的 Raw file 和 Experiment 精确对应；已读取全部 RAW 的文件头。表中其他行是按实验汇总及 Total，未将这些汇总行误当作新增样本。

## 实验组成

| 实验 | RAW 数 | 已确认的材料与设计 |
| --- | --- | --- |
| Purkinje 细胞切片数量比较 | 10 | InCap 为 100/200/400/800 个细胞切片；Spin 为 10/50/100/200/400/800 个细胞切片 |
| Molecular 制备方法比较 | 57 | 小脑分子层组织区域；19 种 collection / digestion / buffer 组合，每种 3 份制备 |
| Betz / Purkinje 比较 | 6 | 各 3 份合样，每份 150 个细胞切片，作者组名为 Cap SP3 |
| 组织参考库 | 3 | 小脑 2 个、运动皮质 1 个，用于配合组织/细胞切片样本的分析 |

论文切取的是薄组织片中的细胞截面；上述数字不能解释为独立单细胞质谱样本。已移除 single-cell 模板、`cells per well=1`、单细胞 ID 和不适用的 FACS、微流控等字段。收集数量按细胞切片记录；分子层组织区域和组织参考库未虚构细胞数。

## 逐文件修正

- RAW 文件头确认全部为 Orbitrap Fusion Lumos。前期 10 个 Purkinje 数量比较运行使用 CID 35 NCE，其余 66 个为 HCD 28 NCE；全部为离子阱 MS2、400–1500 m/z 的 MS1 范围。已修正旧稿统一的 HCD 和明显错误的 `1500% NCE`。
- `summary.txt` 明确只有 56 个 RAW 搜索使用固定 Carbamidomethyl C；其余 20 个没有该固定修饰。两项可变修饰为 Oxidation M 和 Protein N-term Acetyl。`parameters.txt` 支持离子阱碎片容差 0.5 Da；前体搜索容差未直接给出，继续留缺。
- 作者的 Experiment 组名原样保存在 `comment[maxquant experiment]`，并据此恢复材料、收集方式、裂解缓冲液和消化流程因子；作者制备编号另存 `comment[preparation replicate]`。
- 作者 MaxQuant Fraction 值为 1/2/3/10，另列保存，便于复核。正文没有这些样本进行离线分级的步骤，不能把软件编号直接解释为实际第 3 或第 10 个馏分；SDRF 将每份实际运行作为未分级分析记录。
- PALM MicroBeam 为论文注明的 LCM 仪器；组织参考库的具体收集方式未逐文件说明，不将其一并标成 LCM 分选。

## 尚待补齐

论文没有提供供者身份与全部 RAW 的对应；方法比较中的 1/2/3 是制备重复，不能把 76 个文件按出现顺序注释为 76 个生物学重复。生物学重复暂记 `not available`，供者年龄、性别和疾病继续留缺。

Betz/Purkinje 比较的作者组名明确为 Cap SP3，但没有逐文件写出缓冲液；未直接套用正文推荐的 RIPA 条件。三个组织参考库的具体制备也待说明。

由于生物学重复必填项缺失，保留在 `sandbox/`。核对日期：2026-09-27。
