# PXD061414 — under repair

1 coordinate collision remains. The two runs of `LL5176T` differ by an acquisition token (`IDA` vs `NTA`) and by cell input (`4.4E8`), both only in the deposited filenames. The deposit carries no publication reference and its protocol text does not define `NTA`, so the dimension cannot be named faithfully.

Affected file(s): `PXD061414.sdrf.tsv`.

The other defect classes from the first submission (ontology-invalid `characteristics[sample type]`, `NT=`/`AC=` characteristics cells, pandas artifact headers) are fixed in the file above; the coordinate collisions described here are the only remaining blocker.
