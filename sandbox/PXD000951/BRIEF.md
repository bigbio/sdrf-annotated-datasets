# PXD000951：水稻叶绿体激酶鉴定

## 已核实的修正

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD000951)及[文件清单](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD000951/files/all)包含 5 个厂商 RAW。对应的 mzXML 是格式转换结果，不作为额外进样。
- 提交的 [he-total.pep.xml](https://ftp.pride.ebi.ac.uk/pride/data/archive/2015/04/PXD000951/he-total.pep.xml)逐个记录了 RAW 对应的 MGF 和搜索参数；各文件均使用 Trypsin、1 个允许漏切位点、10 ppm 前体容差和 0.6 Da 碎片容差。
- `20081112_14_HE1.RAW` 对应 `F001484.dat`：固定和可变修饰设置均为空。两个修饰列因此使用 `not applicable`，表示本次搜索未设置修饰，不表示样本没有化学修饰。
- 其余 4 个 RAW 均按固定 Carbamidomethyl（C）和可变 Oxidation（M）搜索。原草稿把 Carbamidomethyl 写成可变修饰，现已纠正。HE1、HE2 的原始 Mascot DAT 头部与 pepXML 一致。
- 搜索修饰不能单独证明使用了哪种烷基化试剂；现有可核实协议没有明确给出试剂，撤回原先的 IAA 断言，改为 `not available`。疾病状态也没有直接证据支持 `normal`，改为 `not available`。

## 尚待补齐的证据

- [论文](https://doi.org/10.1093/jxb/eru405)与 PRIDE 协议明确涉及叶绿体肝素亲和富集、凝胶分段和包含列表扫描。草稿现有的单一来源、分级 1–4 及 HE2 重复进样关系，仍需可逐文件追溯的分段记录支持。
- 协议描述切成 5 段，当前清单只有 HE1–HE4 和 HE2 的包含列表进样；不据此补造 HE5 文件。
- 草稿已有的 10 日龄、生长条件以及包含列表进样的采集模式，仍需与完整方法及逐次运行记录核对；本次没有把这些旧字段视作已重新验证。

保留在 `sandbox/`，等待上述样本与分级关系补齐后再转入正式目录。
