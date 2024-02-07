# Alignment-based PARSEVAL Measures
---

We introduce an evaluation system designed to compute PARSEVAL measures, offering a viable alternative to `evalb` (https://nlp.cs.nyu.edu/evalb/) commonly used for constituency parsing evaluation.
The widely used `evalb` script has traditionally been employed for evaluating the accuracy of constituency parsing results, albeit with the requirement for consistent tokenization and sentence boundaries. 
In contrast, our approach, named `jp-evalb`, is founded on an alignment method. This method aligns sentences and words when discrepancies arise.
It aims to overcome several known issues associated with `evalb` by utilizing the **jointly preprocessed (JP)** alignment-based method (`jp-evalb` or Jointly Preprocessed `evalb`).





USAGE:
```
% python3 jp-evalb.py gold_parsed_file system_parsed_file
```

OUTPUT:
- [`Sent. ID`, `Sent. Len.`, `Stat.`] ID, length, and status of the provided sentence, where status 0 indicates 'OK,' status 1 implies 'skip,' and status 2 represents 'error' for `evalb`. `jp-evalb` does not assign skip or error statuses.
- [`Recall`, `Precision`] Recall and precision of constituents.

- [`Matched Bracket`, `Bracket gold`, `Bracket test`] Assessment of matched brackets (true positives) in both the gold and test parsed trees, and their numbers of constituents. 

- [`Cross Bracket`] The number of cross brackets. 

- [`Words`, `Correct Tags`, `Tag Accuracy`] Evaluation of the number of words, correct POS tags, and POS tagging accuracy.


It's important to note that the original `evalb` excludes problematic symbols and punctuation marks in the tree structure. Our results include all tokens in the given sentence, and bracket numbers reflect the actual constituents in the system and gold parse trees. 
Accuracy is determined by comparing the correct number of POS-tagged words to the gold sentence, differing from the original `evalb` which doesn't consider word counts or correct POS tags for punctuation marks. However, we offer an `-evalb` option to precisely replicate `evalb` results, using the `COLLINS.prm` file with its default values (See Case Study 1).


This GitHub repository includes the following case studies: 

1. Evaluation for Section 23 of the English Penn treebank

2. Bug cases identified by `evalb`

3. Korean end-to-end parsing evaluation 



