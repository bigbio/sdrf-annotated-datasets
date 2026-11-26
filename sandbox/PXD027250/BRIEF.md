# PXD027250：三种髓系白血病细胞系的 SWATH 蛋白质组

## 已核实的来源

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD027250)对应[论文 PMID 37253035](https://doi.org/10.1371/journal.pone.0286412)，全文为 [PMC10228771](https://pmc.ncbi.nlm.nih.gov/articles/PMC10228771/)。论文中的蛋白质组实验使用 HL-60、Mo7e、KG-1a 三种人细胞系，比较 CBL0137 处理和对照，以及细胞核、细胞质组分。不能将这些 RAW 直接注释为题名中提到的患者活检样本。
- 归档共有 11 个 WIFF、11 个配套 WIFF.scan、1 个 idx2 和作者的 `SWATH_proteindata_uniprotID.csv`。SDRF 覆盖 11 个实际归档 WIFF。
- 提交记录和论文支持 TripleTOF 6600、SWATH/DIA 和不使用同位素标签的定量。每个 WIFF 的文件头均已读取，包含 `2018_05_03_bML1` 至 `bML11` 的内部路径，但样本标签均为 `Sample1`，未提供细胞系或处理组对应。
- [论文补充资料](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0286412.s002&type=supplementary)中，`S2_File.xlsx` 的 Data 工作表列出三种细胞系、两种处理和两种亚细胞组分的 12 列蛋白质定量值；补充方法 `S1_File.docx` 同时核对。

## 本次修正

- 清除 `FILL` 占位值和空的实验因子列；疾病和生物学重复暂记 `not available`。
- 材料注明 `cell line`，培养细胞的组织来源字段为 `not applicable`。逐文件的具体细胞系、疾病亚型、处理和亚细胞组分尚未补填。
- 使用准确的 DIA 术语、SDRF 3.0 及 ms-proteomics/human 1.1 模板声明。
- 实际消化步骤在已核对的项目记录、正文和补充方法中未找到，旧稿的 Trypsin 改为 `not available`；谱库搜索设置不能单独证明样本实际采用该消化酶。

## 阻断事项

1. 作者定量 CSV 的列名为 `AML1` 至 `AML12`，RAW 文件名为 `bML1` 至 `bML11`。没有公开的逐文件桥接表，不能按数字相同就将两套编号视为同一样本。
2. 论文和补充表描述 12 个生物样本组合，归档只有 11 个 WIFF。缺失的是哪个组合尚未确定，也不能创建不存在的第 12 个 RAW。
3. 生物学重复及实际消化酶仍缺失。当前来源名称仅沿用 RAW 标识；技术重复和馏分均以单次运行表示，未据此建立跨 RAW 的重复或组分关系。

必填字段仍不完整，保留在 `sandbox/`。补齐 RAW 与作者样本编号的对应以及实际消化信息后再重建实验因子和评估是否可以移入正式目录。
