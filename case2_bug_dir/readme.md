```
case2_bug_dir % python3 ../jp-evalb.py bug.gld bug.tst 
START: 2024-01-21 12:01:53.659789
  END: 2024-01-21 12:01:53.716778
```

We evaluate bug cases identified by `evalb`. 
In three cases (sentences 1, 2, and 5), symbols appear, and POS tagging results indicate that these symbols represent words in the system's parsed tree. Consequently, sentence length mismatches arise due to `evalb` discarding symbols during evaluation. 
Our proposed solution involves not disregarding any problematic labels and including symbols as words during evaluation. This approach implies that POS tagging results are based on the entire token numbers. It is noteworthy that `evalb`'s POS tagging results are rooted in the number of words, excluding symbols. 
The two remaining cases (sentences 3 and 4) involve actual word mismatches where trace symbols (*-digit) are inserted into the sentences. 
Naturally, `evalb` cannot handle these cases due to word mismatches. However, as we explained, our proposed algorithm addresses this issue by performing word alignment after sentence alignment.
