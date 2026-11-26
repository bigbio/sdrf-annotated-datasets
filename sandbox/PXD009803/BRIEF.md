# PXD009803：UBR5 与 HTT 泛素化

## 已核实并修正

- [PRIDE 项目](https://www.ebi.ac.uk/pride/archive/projects/PXD009803)和[原论文](https://doi.org/10.1038/s41467-018-05320-3)的质谱方法说明采用抗 HTT 免疫沉淀；补上 `enrichment process=immunoprecipitation`。
- 制备方法直接支持胰蛋白酶柱上消化、DTT 和 IAA；采集方法支持 Q Exactive Plus、HCD 和 27 NCE，5 个 RAW 文件头也确认仪器型号。无标记 CV 及蛋白 N 端乙酰化的目标写法已规范化。
- 提交记录直接列出固定 Carbamidomethyl（C），以及可变 Oxidation（M）、GG（K）、Acetyl（Protein N-term）。论文结果将质谱实验限定为 Q100-HTT 过表达细胞，不能把整篇论文的患者 iPSC 实验背景套入这些 RAW。

## 归档文件与结果表不一致

- `MaxQuant_Output.zip` 的 SHA1 与归档一致。其 `summary.txt` 列出 2017-12-22 的 9 次运行：HTT 对照、HTT-UBR5、HTT-UBR5_death 各 3 次。
- 实际提交的 5 个 RAW 文件头记录 2018-01-10 的运行。UBR5WT_1、_2、_3 分别保留内部 sample_4、_5、_6；UBR5dead_1、_2 分别保留 sample_7、sample_9。两批运行的日期和色谱柱编号不同，不能直接视为同一批文件改名。
- 因此没有把 MaxQuant 的 9 个实验强行映射到这 5 个 RAW，也没有补造缺失对照或第三个 dead RAW。现有重复编号仍需逐样本证据确认。

## 其他未解决事项

- 质谱方法和 PRIDE 写 HEK293，论文通用转染方法写 HEK293T；暂保留质谱方法的 HEK293，尚不能确认其衍生株身份。
- [Cellosaurus HEK293](https://www.cellosaurus.org/CVCL_0045)支持该细胞系的肾来源。来源核对工具的 `organism_part_from_cultured_material` 提示匹配到项目概述中的 iPSC；这不足以否定本组 HEK293 的谱系来源。该提示保留在核查记录中。

结构及解析检查通过。样本及运行对应关系厘清前，保留在 `sandbox/`。
