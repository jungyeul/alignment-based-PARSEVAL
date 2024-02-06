```
case1_ptb23_dir % python3 ../jp-evalb.py 23.gold 23.sys_berkeley_top -evalb 
START: 2024-01-21 12:00:50.199230
  END: 2024-01-21 12:00:54.701044
```

This page shows how to reproduce the original evalb's reuslts by using jp-evalb, and we provide the `diff.txt` file. 
The diff file shows that we reproduced the exactly same results by discarding punctuation marks. 
One sentence result would be different because their token numbers are matched, and evalb could not deal with it:
```
1962 : Length unmatch (19|18)
```
Therefore, the final result for all sentences are different between evalb and jp-evalb.  
