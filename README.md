# Alignment-based PARSEVAL Measures
---
`jp-evalb` or Jointly Preprocessed `evalb`. 


USAGE:
```
% python3 jp-evalb.py gold_parsed_file system_parsed_file
```

OUTPUT:
- [`Sent. ID`, `Sent. Len.`, `Stat.`] ID, length, and status of the provided sentence, where status 0 indicates 'OK,' status 1 implies 'skip,' and status 2 represents 'error' for `evalb`. `jp-evalb` does not assign skip or error statuses.
- [`Recall`, `Precision`] Recall and precision of constituents.

- [`Matched Bracket`, `Bracket gold`, `Bracket test`] Assessment of matched brackets (true positives) in both the gold and test parsed trees, and their numbers of constituents. 

- [`Cross Bracket`] The number of cross brackets. 

- [`Words`, `Correct Tags`, `Tag Accuracy`] Evaluation of the number of words, correct POS tags, and POS tagging accuracy. It's important to highlight that `evalb` excludes any problematic symbols and punctuation marks when counting words and correct POS tags. Our results include all tokens in the given sentence, and accuracy is calculated based on the correct number of POS-tagged words in comparison to the gold sentence.


This GitHub repository includes the following case studies: 

1. Evaluation for Section 23 of the English Penn treebank

2. Bug cases identified by `evalb`

3. Korean end-to-end parsing evaluation 



