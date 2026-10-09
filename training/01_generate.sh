#!/usr/bin/env bash
# Ogretmen ajanla 129 gorev uzerinde eval kosar; traces + PASS/FAIL uretir.
# HARNESS_README "Local CLI Usage" bolumune dayanir.
# NOT: --submission-dir, uretim icin kullandigimiz ajan (ornek: base Gemma +
# cesitlilik icin yuksek temperature'li sampling.yaml). Kendi submission/ ile de
# baslanabilir.

set -e
swegemma eval \
  --tasks        kaggle_data/tasks.jsonl \
  --snapshots-dir kaggle_data/snapshots \
  --submission-dir submission \
  --results-dir   training/results/gen_01 \
  --sandbox       docker \
  --max-tool-calls 60 \
  --max-time-minutes 20 \
  --concurrency   2 \
  --display       auto

# Cesitlilik icin: sampling.yaml'da temperature'i yukselt (0.7-1.0) ve bu
# komutu birkac kez farkli --results-dir ile kosup trajectory havuzunu buyut.
