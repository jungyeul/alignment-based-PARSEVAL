```
case1_ptb23_dir % python3 ../jp-evalb.py 23.gold 23.sys_berkeley_top
START: 2024-01-21 11:22:55.848822
  END: 2024-01-21 11:23:00.334114
```

The parsed results from the Berkeley parser do not contain the TOP symbol as a root. While COLLINS.prm in the original evalb ignores the constituent with TOP, if there is no TOP symbol, it still considers a constituent in evalb. For example, when examining the number of constituents identified from the system for the first sentence in `evalb_wo_top.txt`, evalb indicates 6 constituents, while it actually contains 5 constituents and one empty constituent (, 0, 8).

In jp-errant, we ignore such an empty constituent during the evaluation.
