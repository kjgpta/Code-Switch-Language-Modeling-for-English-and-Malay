#!/bin/bash


# (a) only IMDA part 4 data
# (b) IMDA part 4 + part 5 + part 6
# (c) IMDA part 4 + part 5 + part 6 + Google translation (part 5+part6)
# (d) IMDA part 4 + part 5 + part 6 + Generated CS from part 5 + part6

# assumes ../../imda4-analysis/scripts/preprocess_text_for_analysis.py is already ran

texts_dir=../../imda4-analysis/data/analysis-and-lm-normalized
imda4_train=$texts_dir/combined_train_lm.txt
imda4_val=$texts_dir/combined_val_lm.txt
imda4_test=$texts_dir/combined_test_lm.txt

vocab=../../imda4-analysis/vocab/vocab.txt

order=4
param="-kndiscount -interpolate"
out_dir=../models
eval_outputs=../ppls


# (a) part 4 only to $outdir/lm_a.gz
# build lm
ngram-count -order $order $param -vocab $vocab -unk -sort -text $imda4_train -lm $out_dir/lm_a.gz
#evaluate on val
ngram -debug 2 -order $order -unk -limit-vocab -vocab $vocab -lm $out_dir/lm_a.gz -ppl $imda4_val > $eval_outputs/val_a.ppl
#evaluate on test
ngram -debug 2 -order $order -unk -limit-vocab -vocab $vocab -lm $out_dir/lm_a.gz -ppl $imda4_test > $eval_outputs/test_a.ppl

tail -n 2 $eval_outputs/val_a.ppl
tail -n 2 $eval_outputs/test_a.ppl