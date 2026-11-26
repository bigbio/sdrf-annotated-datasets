# PXD008853：猪腺体特异性唾液

已将映射闭合的 30 行 Orbitrap 子集移入
`datasets/PXD008853/PXD008853-gland-mapped.sdrf.tsv`。本文件保留完整 40
行草稿；标签 116/117 及未处理的 MALDI 分支继续留在 `sandbox/`。

## 已核实并修正

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD008853)及[作者存档论文](https://repository.uantwerpen.be/docman/irua/48a2fa/157665_2020_01_30.pdf)明确样本为腺体分泌的唾液。撤回 `material type=tissue`，并用模板允许重复的 `organism part` 列补充 `saliva`。材料类型枚举没有体液，暂记 `not available`。
- M/SL 样本共同收集下颌腺及单口舌下腺的分泌物。对映射明确的 113、115、119 通道补充舌下腺来源，不能把这类样本理解为单独的下颌腺组织。
- 5 个 RAW 文件头均为 Q Exactive Plus，与详细采集方法一致，已纠正旧仪器字段。
- 4 只猪均为 Belgian Landrace × Piétrain，采样时 21 日龄。表 1 明确猪 1、2 为雌性，猪 3、4 为雄性；仅将性别写入对应关系明确的六个通道。116、117 通道的新增性别及舌下腺来源信息使用 `not available`。
- 没有把年龄转换成未经确认的发育阶段；原 `neonate` 和缺少明确诊断依据的 `normal` 改为 `not available`。8 个单体来源样本在标记后合并，不等于各来源样本事先混合了多个动物，补充 `not pooled`。
- 主分析的 Sus scrofa Mascot DAT 文件头支持既有修饰设置、8 ppm 和 0.8 Da。另一次哺乳类数据库搜索使用 10 ppm，不能声称所有归档搜索都使用 8 ppm。

## 未解决的样本映射

- 提交协议、论文第 2.3 节和[作者学位论文](https://medialibrary.uantwerpen.be/files/9035/11451f59-6c34-4f04-b67f-8b543e9de474.pdf)都存在同一处 116/117 通道标注错位；没有找到独立的原始通道表。
- 这两个通道原有的来源名、动物编号和腺体实验因子仍是旧草稿的待核查值，不能因为交替顺序看起来合理就宣称已验证；新增字段没有沿用这些推断。
- 当前 SDRF 只覆盖五个 Orbitrap RAW、共 40 行。归档还包含 MALDI 分支压缩包，该分支的采集及样本映射尚未处理。

本轮结构及解析检查通过。通道映射和覆盖范围明确前保留在 `sandbox/`，不能直接用作完整研究的定量设计。
