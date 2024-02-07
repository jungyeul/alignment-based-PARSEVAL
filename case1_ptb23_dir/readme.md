```
case1_ptb23_dir % python3 ../jp-evalb.py 23.gold 23.sys_berkeley_top -evalb 
START: 2024-01-21 12:00:50.199230
  END: 2024-01-21 12:00:54.701044
```

This page demonstrates how to replicate the original results from `evalb` using `jp-evalb`. The parsed results were obtained using the PCFG-LA Berkeley parser. We provide the `diff.txt` file, which indicates that we have successfully reproduced the exact results by excluding punctuation marks. However, there may be a discrepancy in a single sentence due to mismatching token numbers, which `evalb` cannot handle. Consequently, the final results for all sentences differ between evalb (`evalb.txt`) and jp-evalb (`jp-evalb-original.txt`).
```
1962 : Length unmatch (19|18)
```

