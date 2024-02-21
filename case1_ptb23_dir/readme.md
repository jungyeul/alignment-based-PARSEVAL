```
case1_ptb23_dir % python3 ../jp-evalb.py 23.gold 23.sys_berkeley_top -evalb COLLINS.prm
```

This page demonstrates how to replicate the original results from `evalb` using `jp-evalb` with the `-evalb` option. The parsed results were obtained using the PCFG-LA Berkeley parser. When the parameter file is not provided, this option can utilize the default values from the `COLLINS.prm` file. It will accurately reproduce evalb results, even in cases where discrepancies such as Length unmatch and Words unmatch errors occur in evalb's output.


We also present Dan Bikel's `compare.pl` comparison results between `evalb` and `jp-evalb` using the `-evalb` option, demonstrating their identical outcomes:
```
case1_ptb23_dir % perl compare.pl evalb.txt jp-evalb-legacy.txt 
43993
model1: recall=89.7986405660151, precision=90.3007371627303
model2: recall=89.7986405660151, precision=90.3007371627303
model2 recall - model1 recall = 0
model2 precision - model1 precision = 0
Doing random shuffle 10000 times.
Completed 1000 iterations
Completed 2000 iterations
Completed 3000 iterations
Completed 4000 iterations
Completed 5000 iterations
Completed 6000 iterations
Completed 7000 iterations
Completed 8000 iterations
Completed 9000 iterations
number of random recall diferences equal to or greater than
	original observed difference: 10000
number of random precision diferences equal to or greater than
	original observed difference: 10000
p-value for recall diff: 1
p-value for precision diff: 1
p-value for Fscore diff: 1 
```
