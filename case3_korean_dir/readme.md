```
case3_korean_dir % python3 ../jp-evalb.py BGAA0001.test.gold BGAA0001.test.sys 
START: 2024-01-21 12:02:24.911305
  END: 2024-01-21 12:02:25.390114
```


We perform a thorough parsing evaluation for Korean, wherein the sequences of sentences and tokens, system-segmented for use as constituency parsing input, may diverge from the corresponding gold sequences of sentences and tokens.
We utilized the following resources for our parsing evaluation to simulate the end-to-end process:

1. A set of 148 test sentences with 4538 tokens (morphemes)  from `BGAA0001` of the Korean Sejong treebank, as detailed in {kim-park:2022}. In the present experiment, all sentences have been consolidated into a single text block. 

2. POS tagging performed by `sjmorph.model` {park-tyers:2019:LAW} for morpheme segmentation (https://github.com/jungyeul/sjmorph). The model's pipeline includes sentence boundary detection and tokenization through morphological analysis, generating an input format for the parser. 

3. A Berkeley parser model for Korean trained on the Korean Sejong treebank {park-hong-cha:2016:PACLIC} (https://zenodo.org/records/3995084).

Given our sentence boundary detection and tokenization processes, there is a possibility of encountering sentence and word mismatches during constituency parsing evaluation. The system results show 123 sentences and 4367 morphemes because differences in sentence boundaries and tokenization results. During the evaluation, `jp-evalb` successfully aligns even in the presence of sentence and word mismatches, and subsequently, the results of constituency parsing are assessed. 



- Kim, M., & Park, J. (2022). A note on constituent parsing for Korean. Natural Language Engineering, 28(2), 199–222. https://doi.org/10.1017/S1351324920000479
- Park, J., & Tyers, F. (2019). A New Annotation Scheme for the Sejong Part-of-speech Tagged Corpus. Proceedings of the 13th Linguistic Annotation Workshop, 195–202. https://www.aclweb.org/anthology/W19-4022
- Park, J., Hong, J.-P., & Cha, J.-W. (2016). Korean Language Resources for Everyone. Proceedings of the 30th Pacific Asia Conference on Language, Information and Computation: Oral Papers (PACLIC 30), 49–58. http://aclweb.org/anthology/Y/Y16/Y16-2002.pdf


