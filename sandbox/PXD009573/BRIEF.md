# PXD009573：SMARCA4 体外磷酸化实验

## 已核实并修正

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD009573)及[原论文](https://doi.org/10.1016/j.cell.2018.09.051)说明这里提交的是纯化蛋白的体外实验。将不合适的 `material type=tissue` 改为 `not available`：当前模板枚举没有纯化蛋白这一类。
- 5 个 RAW 文件头均支持 Orbitrap Elite、CID 和离子阱 MS2。归档 mzML 仅包含一个来自 SMARCA4 1 小时组的谱图，同样标注 CID；文件名中的 `ETD_CID` 不能单独证明实际使用了 ETD。
- mzIdentML 列出的 5 个 RAW 与归档文件对应；两个含药物的内部文件名保留 `+MC180295`，公开归档文件名省略了加号。SDRF 使用归档名称。
- 统一无标记样本的 CV 写法，补上碎裂方式和 MS2 分析器。提交记录支持前体容差 20 ppm、碎片容差 0.4 Da，以及可变磷酸化 S/T/Y。

## 尚待核实

- 提交记录、论文方法和 mzIdentML 将 Trypsin 列为搜索酶；样本制备只写 in-StageTip 消化，没有直接给出实际使用的消化酶。旧草稿的 Trypsin 尚不能作为已验证的制备条件。来源核对工具对此仍报 `cleavage_agent_unsupported`。
- RAW 名称明确区分 alone、30 分钟、1 小时及 MC180295 条件，但独立蛋白制备批次、重复关系，以及 alone 对照的完整处理过程尚未确认。旧草稿的生物学重复 1 未获得独立证据。

结构及解析检查通过。上述科学证据缺口补齐前，保留在 `sandbox/`。
