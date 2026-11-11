# PXD000021：合成磷酸肽混合物的碎裂与定位评分比较

来源：[PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD000021)、[D-score 论文](https://doi.org/10.1002/pmic.201200408)及其数据来源 [Savitski 等的原实验](https://pmc.ncbi.nlm.nih.gov/articles/PMC3033680/)。这是五组化学合成磷酸肽混合物的再分析；数据库中的人源蛋白序列不能被解释为实际采集了人细胞。

## 已修正

- 全部 16 个归档 RAW 均已读取文件头，仪器为 **LTQ Orbitrap XL**。按作者五个混合物及 RAW 中的混合物编号，统一两种文件名前缀 `Pepmix` / `ppeptidemix` 的来源标识。
- 材料类型改为 `synthetic`；物种、解剖部位和实际消化酶为 `not applicable`。原论文的方法明确先合成肽，再直接进行 LC-MS/MS；Mascot 的 Trypsin 是搜索规则，不能据此声称样本进行过 Trypsin 消化。
- 文件头证实 3 个 ETD 运行关闭补充激活，4 个 `_ETD_2` 运行开启补充激活；另外有 3 个 HCD、3 个 CID 和 3 个 MSA 运行。MSA 的中性丢失激活列表也已核实。`_2` 不是新的生物学重复。
- HCD 为 Orbitrap MS2，其他方法为离子阱 MS2。HCD 和 CID/MSA 的碰撞能分别为 40 和 35 NCE；未将 ETD 方法中保存的 CID 参数误记成 ETD 碰撞能。
- 16 份作者 Mascot DAT 参数头一致：固定 Carbamidomethyl C，可变 Oxidation M、Phospho S/T/Y。已清除旧稿中没有 Mascot 搜索依据的 Acetyl、Methyl/Monohydroxylation 混写和 pyro-Glu 项，并补全 Phospho 位点。前体容差为 10 ppm；HCD 碎片容差为 0.02 Da，其余为 0.5 Da。SDRF 的修饰与容差列表示此次 Mascot 重分析的设置；项目另外归档了 X!Tandem 和 OMSSA 结果。

## 重复与模板限制

每组混合物的各个碎裂方式都是一次独立采集，SDRF 用实验因子区分；不将方法差异增加为生物学重复。合成肽没有生物学重复，故记录 `not applicable`。当前 sample-metadata 模板要求该字段为整数或 `pooled`，不接受 `not applicable`。

本项目没有需要据此补造的生物学重复。保留在 `sandbox/`，待合成材料的重复编码约定明确后再考虑正式入库；未为通过模板而填写虚构的生物学编号。核对日期：2026-09-27。
