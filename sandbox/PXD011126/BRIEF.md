# PXD011126：Flag-MPP9 相互作用蛋白

## 已核实并补充

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD011126)和[原论文](https://doi.org/10.1038/s41467-018-06990-9)一致说明质谱样本来自过表达 Flag-MPP9 的 HEK293T 细胞。补上转染及免疫沉淀字段，来源名称保留细胞系和诱饵背景。
- 论文方法确认 DMEM 培养、抗 Flag 免疫沉淀、凝胶条带切取和胰蛋白酶消化。补充图 3a 进一步明确：用于互作筛选的质谱条带来自 Flag-MPP9 组特异条带，不能把空载体泳道直接扩展为已提交的 RAW。
- 5 个 RAW 文件头均支持 Orbitrap Elite 和 CID。提交方法支持 DTT/IAA、前体容差 5 ppm、碎片容差 0.6 Da，以及固定 Carbamidomethyl（C）和可变 Oxidation（M）。
- [Cellosaurus CVCL_0063](https://www.cellosaurus.org/CVCL_0063)支持 HEK293T 的女性、胎儿来源信息；没有据此编造数值年龄。

## 尚待核实

- `14-312_HN1208_1.raw` 至 `_5.raw` 的逐条带对应关系和独立制备批次没有在已取得的正文、补充图或五个蛋白结果 CSV 中明确给出。
- 单一来源、生物学重复 1、分段编号 1 至 5 仍沿用旧草稿，尚不能视为已确认的实验设计。CSV 中反复检出 MPP9 也不能替代样本对应表。

本轮结构及解析检查通过，保留 `no_factor_value` 提示。上述缺口补齐前保留在 `sandbox/`。
