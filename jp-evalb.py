import datetime
import os
import sys
from collections import defaultdict
from nltk.tree import *


# # check the arguments
# assert len(sys.argv) == 3, "Usage: python jp-evalb.py gold_file_name sys_file_name"
# gold_file_name = os.path.join(os.getcwd(), sys.argv[1])
# sys_file_name = os.path.join(os.getcwd(), sys.argv[2])

# global configuration for the evaluation
DELETED_LABELS_COLLINS = {"TOP", "-NONE-", ",", ":", "``", "''", "."}
DELETED_LABELS_NEW = DELETED_LABELS_COLLINS | {"S1", "?", "!"}

english_token_exception = {'\'\'':'\"',  '`':'\'', '``': '\"', 'ca': 'can', 'wo':'will', 'n\'t':'not'}

DELETED_LABELS = None
CHECK_CONS_LABELS = True
LANGUAGE = 'default'
IGNORE_EMPTY_CONS = True
EVALB = False

TOTAL_match = 0
TOTAL_bn1 = 0
TOTAL_bn2 = 0
TOTAL_crossing = 0
TOTAL_no_crossing = 0
TOTAL_2L_crossing = 0

TOTAL_word = 0
TOTAL_correct_tag = 0

TOTAL_sent = 0
TOTAL_error_sent = 0
TOTAL_skip_sent = 0
TOTAL_comp_sent = 0

TOT40_match = 0
TOT40_bn1 = 0
TOT40_bn2 = 0
TOT40_crossing = 0
TOT40_no_crossing = 0
TOT40_2L_crossing = 0

TOT40_word = 0
TOT40_correct_tag = 0

TOT40_sent = 0
TOT40_error_sent = 0
TOT40_skip_sent = 0
TOT40_comp_sent = 0

SYS_PUNC_CNT = []
GOLD_PUNC_CNT = []

# Helper class for writing to file
class EvalFileWriter:
    _EVALB_HEADER = "  Sent.                        Matched  Bracket   Cross        Correct Tag\n"+ \
                   " ID  Len.  Stat. Recal  Prec.  Bracket gold test Bracket Words  Tags Accracy\n"
                   
    _SEP_LINE = "============================================================================\n"
    
    _LINE_FORMAT = "{:>4} {:>4} {:>4} {:>7.2f} {:>6.2f} {:>5} {:>6} {:>4} {:>6} {:>6} {:>5} {:>8.2f}"
    
    
    def write_line(self, line_to_write):
        try:
            with open(self._file_name, 'a', encoding='utf-8') as file:
                file.write(line_to_write)
                file.flush()
        except IOError as e:
            print('Error writing to file: ' + self._file_name)
            print(e)
            assert False
    
    def clear_file(self):
        try:
            with open(self._file_name, 'a', encoding='utf-8') as file:
                file.truncate(0)
                file.flush()
        except IOError as e:
            print('Error writing to file: ' + self._file_name)
            print(e)
            assert False
    
    def write_current_time(self) -> None:
        time = datetime.datetime.utcnow()
        time_str = time.strftime("%m/%d/%y %H:%M:%S.") + "{:06d}".format(time.microsecond) + "000 UTC"
        self.write_line("Current time: " + time_str + '\n')
    
    def write_header(self):
        self.write_line(self._EVALB_HEADER)
        self.write_line(self._SEP_LINE)
        
    def write_eval_line(self, eval_result):
        result_line = self._LINE_FORMAT.format(*eval_result)
        self.write_line(result_line + '\n')
    
    def write_eval_output(self):
        global TOTAL_match, TOTAL_bn1, TOTAL_bn2, TOTAL_crossing, TOTAL_no_crossing
        
        self.write_line(self._SEP_LINE)
        output = ""
    
        if TOTAL_bn1 > 0 and TOTAL_bn2 > 0:
            output += "                {:6.2f} {:6.2f} {:5d} {:5d} {:5d}  {:5d}".format(
                100.0 * TOTAL_match / TOTAL_bn1 if TOTAL_bn1 > 0 else 0.0,
                100.0 * TOTAL_match / TOTAL_bn2 if TOTAL_bn2 > 0 else 0.0,
                TOTAL_match,
                TOTAL_bn1,
                TOTAL_bn2,
                TOTAL_crossing
            )

        output += "  {:5d} {:5d}   {:6.2f}".format(
            TOTAL_word,
            TOTAL_correct_tag,
            100.0 * TOTAL_correct_tag / TOTAL_word if TOTAL_word > 0 else 0.0
        )

        output += "\n"
        self.write_line(output)
        
    def write_eval_summary(self):
        
        global TOTAL_sent, TOTAL_error_sent, TOTAL_skip_sent, TOTAL_comp_sent
        
        self.write_line("=== Summary ===\n\n")

        sentn = TOTAL_sent - TOTAL_error_sent - TOTAL_skip_sent

        self.write_line("-- All --\n")
        self.write_line("Number of sentence        = {:6d}\n".format(TOTAL_sent))
        self.write_line("Number of Error sentence  = {:6d}\n".format(TOTAL_error_sent))
        self.write_line("Number of Skip  sentence  = {:6d}\n".format(TOTAL_skip_sent))
        self.write_line("Number of Valid sentence  = {:6d}\n".format(sentn))

        r = 100.0 * TOTAL_match / TOTAL_bn1 if TOTAL_bn1 > 0 else 0.0
        self.write_line("Bracketing Recall         = {:6.2f}\n".format(r))

        p = 100.0 * TOTAL_match / TOTAL_bn2 if TOTAL_bn2 > 0 else 0.0
        self.write_line("Bracketing Precision      = {:6.2f}\n".format(p))

        f = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        self.write_line("Bracketing FMeasure       = {:6.2f}\n".format(f))

        self.write_line("Complete match            = {:6.2f}\n".format(100.0 * TOTAL_comp_sent / sentn if sentn > 0 else 0.0))
        self.write_line("Average crossing          = {:6.2f}\n".format(1.0 * TOTAL_crossing / sentn if sentn > 0 else 0.0))
        self.write_line("No crossing               = {:6.2f}\n".format(100.0 * TOTAL_no_crossing / sentn if sentn > 0 else 0.0))
        self.write_line("2 or less crossing        = {:6.2f}\n".format(100.0 * TOTAL_2L_crossing / sentn if sentn > 0 else 0.0))
        self.write_line("Tagging accuracy          = {:6.2f}\n".format(100.0 * TOTAL_correct_tag / TOTAL_word if TOTAL_word > 0 else 0.0))

        TOT_cut_len = 40

        sentn = TOT40_sent - TOT40_error_sent - TOT40_skip_sent

        self.write_line("\n-- len<={} --\n".format(TOT_cut_len))
        self.write_line("Number of sentence        = {:6d}\n".format(TOT40_sent))
        self.write_line("Number of Error sentence  = {:6d}\n".format(TOT40_error_sent))
        self.write_line("Number of Skip  sentence  = {:6d}\n".format(TOT40_skip_sent))
        self.write_line("Number of Valid sentence  = {:6d}\n".format(sentn))

        r = 100.0 * TOT40_match / TOT40_bn1 if TOT40_bn1 > 0 else 0.0
        self.write_line("Bracketing Recall         = {:6.2f}\n".format(r))

        p = 100.0 * TOT40_match / TOT40_bn2 if TOT40_bn2 > 0 else 0.0
        self.write_line("Bracketing Precision      = {:6.2f}\n".format(p))

        f = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        self.write_line("Bracketing FMeasure       = {:6.2f}\n".format(f))

        self.write_line("Complete match            = {:6.2f}\n".format(100.0 * TOT40_comp_sent / sentn if sentn > 0 else 0.0))
        self.write_line("Average crossing          = {:6.2f}\n".format(1.0 * TOT40_crossing / sentn if sentn > 0 else 0.0))
        self.write_line("No crossing               = {:6.2f}\n".format(100.0 * TOT40_no_crossing / sentn if sentn > 0 else 0.0))
        self.write_line("2 or less crossing        = {:6.2f}\n".format(100.0 * TOT40_2L_crossing / sentn if sentn > 0 else 0.0))
        self.write_line("Tagging accuracy          = {:6.2f}\n".format(100.0 * TOT40_correct_tag / TOT40_word if TOT40_word > 0 else 0.0))

        self.write_current_time()
    
    def __init__(self, file_name):
        self._file_name = file_name
        self.clear_file()


def clean_tree(tree, punc_cnt):
    LABEL_TO_DELETE = DELETED_LABELS_COLLINS
    if len(tree) == 1 and isinstance(tree[0], str):
        return tree
    else:
        new_tree = Tree(tree.label(), [])
        for subtree in tree:
            if subtree.label() not in LABEL_TO_DELETE:
                new_tree.append(clean_tree(subtree, punc_cnt))
            else:
                punc_cnt[-1] += 1
        return new_tree


# function for extracting leaves and trees from the parsed data
def extract_leaves_and_trees(sys, gold): # parsed (L) and parsed_gold (R) "lists";
    L_trees = []
    R_trees = []
    L_leaves = []
    R_leaves = []

    for tree_string in sys:
        tree = Tree.fromstring(tree_string)
        if len(tree) > 1:
            tree = Tree('TOP', [tree])

        leaves = tree.leaves()
        L_trees.append(tree)
        # join and lowercase all words
        L_leaves.append(" ".join(leaves).lower())

    for tree_string in gold:
        tree = Tree.fromstring(tree_string)
        if len(tree) > 1:
            tree = Tree('TOP', [tree])

        leaves = tree.leaves()
        R_trees.append(tree)
        R_leaves.append(" ".join(leaves).lower())

    if EVALB:
        temp = []
        for tree in L_trees:
            SYS_PUNC_CNT.append(0)
            temp.append(clean_tree(tree, SYS_PUNC_CNT))
        L_trees = temp
        temp = []
        for tree in R_trees:
            GOLD_PUNC_CNT.append(0)
            temp.append(clean_tree(tree, GOLD_PUNC_CNT))
        R_trees = temp

    return L_trees, R_trees, L_leaves, R_leaves

def token_check(leaves):
    leaves_tok = []
    for tok in leaves.split(' '):
        if tok in english_token_exception:
            leaves_tok.append(english_token_exception[tok])
        else:
            leaves_tok.append(tok)
    return leaves_tok

def edit_dis_ratio(token_list1, token_list2):
    str1 = "".join(token_list1)
    str2 = "".join(token_list2)
    
    m, n = len(str1), len(str2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],
                                   dp[i - 1][j],
                                   dp[i - 1][j - 1])

    dis_ratio = dp[m][n]/len(str2)

    return dis_ratio


def sentence_alignment(L_trees, R_trees, L_leaves, R_leaves):

    a = L_leaves
    b = R_leaves

    L_aligned = []
    R_aligned = []
    L_trees_aligned = []
    R_trees_aligned = []

    l_prime = []
    r_prime = []
    l_tree_prime = []
    r_tree_prime = []

    ii = 0
    jj = 0
    
    def recur_check(i, j):
        a_tokens = token_check(a[i])
        b_tokens = token_check(b[j])
        if "".join(a_tokens) == "".join(b_tokens):
            return True
        elif edit_dis_ratio(a_tokens, b_tokens) <= 0.15:
            return (i >= len(a) and j >= len(b)) or recur_check(i+1, j+1)
        else:
            return False


    for i in range(0, len(a)+1):
        i = ii
        for j in range(i, len(b)+1):
            j = jj
            # print('>', i, j)

            # checking a_i and b_j are same
            # if a[i] == b[j]:
            if recur_check(i, j):
                L_aligned.append(a[i])
                R_aligned.append(b[j])
                L_trees_aligned.append(L_trees[i])
                R_trees_aligned.append(R_trees[j])
                # print(L_aligned, R_aligned)
                # print(L_trees_aligned, R_trees_aligned)
                
                ii = i+1
                jj = j+1
                break
            else:
                l_prime.append(a[i])
                r_prime.append(b[j])
                l_tree_prime.append(L_trees[i])
                r_tree_prime.append(R_trees[j])

                if len(a) == i+1 and len(b) == j+1:
                    L_aligned.append(a[i])
                    R_aligned.append(b[j])
                    L_trees_aligned.append(L_trees[i])
                    R_trees_aligned.append(R_trees[j])
                    # print(L_aligned, R_aligned)
                    # print(L_trees_aligned, R_trees_aligned)
                    ii = i+1
                    jj = j+1
                    break
                else:
                    # checking if a_i+1 and b_j+1 are same <-- stop condition
                    while not recur_check(i+1, j+1):
                        if len(a[i]) < len(b[j]):
                            i += 1
                            l_prime.append(a[i])
                            l_tree_prime.append(L_trees[i])
                        elif len(a[i]) > len(b[j]):
                            j += 1
                            r_prime.append(b[j])
                            r_tree_prime.append(R_trees[j])
                        else:
                            break
                    L_aligned.append(l_prime)
                    R_aligned.append(r_prime)
                    L_trees_aligned.append(l_tree_prime)
                    R_trees_aligned.append(r_tree_prime)
                    # print(L_aligned, R_aligned)
                    # print(L_trees_aligned, R_trees_aligned)
                    l_prime = []
                    r_prime = []
                    l_tree_prime = []
                    r_tree_prime = []

                    ii = i+1
                    jj = j+1
                    break
                    
        if ii == len(a) and jj == len(b):
            break
        
    assert len(L_trees_aligned) == len(R_trees_aligned)
    assert len(L_aligned) == len(R_aligned)
    return L_trees_aligned, R_trees_aligned, L_aligned, R_aligned


# function for merging the trees
def merging_trees(tree_list):
    reindexed_tree = []
    for tree in tree_list:
        if list(tree) == tree:
            reindexed_tree.append(Tree('TOP', tree))
        else:
            reindexed_tree.append(tree)

    return reindexed_tree

# function for flattening the list
def flatten(l):
    return [item for sublist in l for item in sublist]

# function for word alignment
def word_alignment_by_sent(l, r):

    L = []
    R = []
    a = l 
    b = r 
    l_prime = []
    r_prime = []
    ii = 0
    jj = 0

    for i in range(0, len(a)+1):

        if ii >= len(a) or jj >= len(b):
            if jj >= len(b):
                aa = []
                for iii in range(ii, len(a)):
                    aa.append(a[iii])
                if len(L) == 0:
                    L = aa
                else:
                    L[-1] = L[-1] + aa

            elif ii >= len(a):
                bb = []
                for jjj in range(jj, len(b)):
                    bb.append(b[jjj])
                if len(R) == 0:
                    R = bb
                else:
                    R[-1] = [R[-1]] + bb
                

            # print(a[ii:])
            # print(b[jj:])
            # print('out of range')
            break

        i = ii
        # print('i>', i)

        for j in range(jj, len(b)+1):
            j = jj
            if a[i].lower() == b[j].lower():
                L.append(a[i])
                R.append(b[j])                
                # print(L, R)
                ii = i+1
                jj = j+1
                break
            else:
                l_prime.append(a[i])
                r_prime.append(b[j])

                if len(a) == i+1 and len(b) == j+1:
                    L.append(a[i])
                    R.append(b[j])
                    # print(L, R)
                    ii = i+1
                    jj = j+1
                    break
                else:
                    # adding stop condition for the end of the list; 
                    if len(a) == i+1 or len(b) == j+1:
                        if  len(a) == i+1 and len(b) == j+1:
                            L.append(a[i])
                            R.append(b[j])
                            ii = i+1
                            jj = j+1
                        elif len(a) == i+1:
                            aa = []
                            aa.append(a[i])
                            L.append(aa)
                            bb = []
                            for jjj in range(j,len(b)):
                               bb.append(b[jjj])
                               j += 1
                            R.append(bb)
                            ii = i+1
                            jj = j

                        elif len(b) == j+1:
                            bb = []
                            bb.append(b[j])
                            R.append(bb)
                            aa = []
                            for iii in range(i,len(a)):
                               aa.append(a[iii])
                               i += 1
                            L.append(aa)
                            ii = i
                            jj = j+1 
                        break
                    else:
                        # checking if a_i+1 and b_j+1 are same <-- stop condition
                        while a[i+1].lower() != b[j+1].lower():
                            L_length = len(''.join(flatten(L)))
                            left_length = len(''.join(a)) - L_length - len(''.join(l_prime))
                            R_length = len(''.join(flatten(R)))
                            right_length = len(''.join(b)) - R_length - len(''.join(r_prime))
                            if left_length > right_length:
                                i += 1
                                l_prime.append(a[i])
                            elif left_length < right_length:
                                j += 1
                                r_prime.append(b[j])
                            else:
                                break

                        L.append(l_prime)
                        R.append(r_prime)
                        # print(L, R)
                        l_prime = []
                        r_prime = []

                        ii = i+1
                        jj = j+1
                        break
                        
        # print('iijj>', ii, jj, len(a), len(b))
        if ii == len(a) and jj == len(b):
            break
   
    # assert len(L) == len(R)
    return L, R

# wrapping function for the entire list
def word_alignment(L_trees_merged, R_trees_merged):
    L_word_aligned = []
    R_word_aligned = []

    for i, j in zip(L_trees_merged, R_trees_merged):
        l = i.leaves()
        r = j.leaves()
        
        L, R = word_alignment_by_sent(l,r)
        
        L_word_aligned.append(L)
        R_word_aligned.append(R)

    return L_word_aligned, R_word_aligned

# function for getting the constituents
def get_constituents(tree,start_index=0):
    if EVALB:
        constituents = list()
    else:
        constituents = set()
    
    if tree.height() > 2:
        end_index = start_index + len(tree.leaves())
        if EVALB:
            constituents.append((tree.label(), start_index, end_index, " ".join(tree.leaves())))
        else:
            constituents.add((tree.label(), start_index, end_index, " ".join(tree.leaves())))


        for phrase in tree:
            if EVALB:
                constituents.extend(get_constituents(phrase, start_index))
            else:
                constituents.update(get_constituents(phrase, start_index))
            start_index += len(phrase.leaves())
            
    return constituents

# function for reindexing the constituents
def get_constituents_by_reindexing(L_trees_merged, R_trees_merged, L_word_aligned, R_word_aligned):

    L_constituents = []
    R_constituents = []
    L_constituents_index_only = []
    R_constituents_index_only = []

    for idx, (i, j) in enumerate(zip(L_word_aligned, L_trees_merged)):
        words_list = i 

        reindexed_words_list = []
        for ii in range(len(words_list)):
            if isinstance(words_list[ii], list):
                for jj in range(len(words_list[ii])):
                    words_list[ii][jj] = str(ii) + "." + str(jj) + "|" + words_list[ii][jj]
                    reindexed_words_list.append(words_list[ii][jj])
            else: 
                words_list[ii] = str(ii)  + "|" + words_list[ii]
                reindexed_words_list.append(words_list[ii])
        # print(words_list)
        # print(reindexed_words_list)

        tree = j 

        assert len(reindexed_words_list) == len(tree.leaves())


        constituents = get_constituents(tree)

        reindexed_constituents = []
        index_only_constituents = []
        for const in constituents:
            # print('<', const)
            label = const[0]
            # print(label)
            if label == 'TOP':
                pass
            else:
                if '-' in label:
                    label = label.split('-')[0]
                s = const[1]
                start = int(s) 
                start_index = reindexed_words_list[start].split('|')[0]
                if '.' in start_index:
                    start_index = start_index.split('.')[0]
                e = const[2]
                end = int(e) - 1
                end_index = reindexed_words_list[end].split('|')[0]
                if '.' in end_index:
                    end_index = end_index.split('.')[0]
                word = const[3]

                constituent = (label, int(start_index), int(end_index)+1, word)
                index_only = (label, int(start_index), int(end_index)+1)
                # print('>', constituent)
                reindexed_constituents.append(constituent)
                index_only_constituents.append(index_only)
        L_constituents.append(reindexed_constituents)
        L_constituents_index_only.append(index_only_constituents)


    for idx, (i, j) in enumerate(zip(R_word_aligned, R_trees_merged)):
        words_list = i 

        reindexed_words_list = []
        for ii in range(len(words_list)):
            if isinstance(words_list[ii], list):
                for jj in range(len(words_list[ii])):
                    # print('ii-jj>',  ii, jj, words_list[ii][jj])
                    words_list[ii][jj] = str(ii) + "." + str(jj) + "|" + words_list[ii][jj]
                    reindexed_words_list.append(words_list[ii][jj])
            else: 
                # print('ii>', ii, words_list[ii])
                words_list[ii] = str(ii)  + "|" + words_list[ii]
                reindexed_words_list.append(words_list[ii])
        # print(words_list)
        # print(reindexed_words_list)

        tree = j 
        assert len(reindexed_words_list) == len(tree.leaves())
        # print(tree.leaves())

        constituents = get_constituents(tree)

        reindexed_constituents = [] 
        index_only_constituents = []
        for const in constituents:
            # print('<', const)
            label = const[0]
            # print(label)
            if label == 'TOP':
                pass
            else:
                if '-' in label:
                    label = label.split('-')[0]
                s = const[1]
                start = int(s) 
                start_index = reindexed_words_list[start].split('|')[0]
                if '.' in start_index:
                    start_index = start_index.split('.')[0]
                e = const[2]
                end = int(e) - 1
                end_index = reindexed_words_list[end].split('|')[0]
                if '.' in end_index:
                    end_index = end_index.split('.')[0]
                word = const[3]

                constituent = (label, int(start_index), int(end_index)+1, word)
                index_only = (label, int(start_index), int(end_index)+1)
                # print('>', constituent)
                reindexed_constituents.append(constituent)
                index_only_constituents.append(index_only)
        R_constituents.append(reindexed_constituents)
        R_constituents_index_only.append(index_only_constituents)

    return L_constituents, R_constituents, L_constituents_index_only, R_constituents_index_only

# function for traversing the tree
def traverse_tree(tree):
    if EVALB:
        DELETED_LABELS = DELETED_LABELS_COLLINS
    else:
        DELETED_LABELS = None
    if len(tree) == 1 and isinstance(tree[0], str):
        if DELETED_LABELS is None or tree.label() not in DELETED_LABELS:
            return [(tree.label(), tree[0])]
        else:
            return []
    else:
        result = []
        for subtree in tree:
            result += traverse_tree(subtree)
        return result

# function for calculating the bracket
def cal_bracket(sys_cons, gold_cons):
    if CHECK_CONS_LABELS:
        matched_bracket = len(set(sys_cons) & set(gold_cons))
        if EVALB:
            left = set(sys_cons) - set(gold_cons)
            right = set(gold_cons) - set(sys_cons)
            cnt = 0
            for con1 in left:
                for con2 in right:
                    if con1[1] == con2[1] and con1[2] == con2[2] and set([con1[0], con2[0]]) == set(["ADVP", "PRT"]):
                        cnt += 1

            matched_bracket += cnt
    else:
        matched_bracket = len(set([(tup[1], tup[2]) for tup in sys_cons]) & set([(tup[1], tup[2]) for tup in gold_cons]))
    
    cross_bracket = 0
    for i, sys_con in enumerate(sys_cons):
        for j, gold_con in enumerate(gold_cons):
            if sys_con[1] < gold_con[1] < sys_con[2] < gold_con[2] or gold_con[1] < sys_con[1] < gold_con[2] < sys_con[2]:
                cross_bracket += 1
                break
    
    return matched_bracket, cross_bracket

# function for getting the evaluation result
def get_eval_result(id, sys_words, gold_words, sys_cons, gold_cons, sys_tree, gold_tree):
    global TOTAL_match, TOTAL_bn1, TOTAL_bn2, TOTAL_crossing, TOTAL_no_crossing
    global TOTAL_2L_crossing, TOTAL_word, TOTAL_correct_tag
    global TOTAL_sent, TOTAL_error_sent, TOTAL_skip_sent, TOTAL_comp_sent
    
    global TOT40_match, TOT40_bn1, TOT40_bn2, TOT40_crossing, TOT40_no_crossing
    global TOT40_2L_crossing, TOT40_word, TOT40_correct_tag
    global TOT40_sent, TOT40_error_sent, TOT40_skip_sent, TOT40_comp_sent
    
    if IGNORE_EMPTY_CONS:
        sys_cons = [con for con in sys_cons if con[0] != ""]
        gold_cons = [con for con in gold_cons if con[0] != ""]
    
    matched_bracket, cross_bracket = cal_bracket(sys_cons, gold_cons)
    sys_tags = traverse_tree(sys_tree)
    gold_tags = traverse_tree(gold_tree)
    
    gold_tags_cnt = defaultdict(int)
    
    for tag in gold_tags:
        gold_tags_cnt[tag] += 1
    
    sys_tags_cnt = defaultdict(int)
    for tag in sys_tags:
        sys_tags_cnt[tag] += 1
    
    tags_tp = sum([min(gold_tags_cnt[tag], sys_tags_cnt[tag]) for tag in sys_tags_cnt])
    if LANGUAGE == "en" or EVALB:
        tags_tp = sum([sys_tags[i] == gold_tags[i] for i in range(len(sys_tags))])

    TOTAL_match += matched_bracket
    TOTAL_bn1 += len(gold_cons)
    TOTAL_bn2 += len(sys_cons)
    TOTAL_crossing += cross_bracket
    TOTAL_no_crossing += (cross_bracket == 0)
    TOTAL_2L_crossing += (cross_bracket <= 2)
    
    TOTAL_word += len(gold_tags)
    TOTAL_correct_tag += tags_tp

    # ID
    result = [id]
    # Len.
    if EVALB:
        result.append(len(gold_words) + GOLD_PUNC_CNT[id - 1])
    else:
        result.append(len(gold_words))
    # Stat.
    result.append(0)
    # Recal
    result.append(matched_bracket/len(gold_cons)*100 if len(gold_cons) else 0)
    # Prec.
    result.append(matched_bracket/len(sys_cons)*100 if len(sys_cons) else 0)
    
    # Matched Bracket
    result.append(matched_bracket)
    # Bracket gold
    result.append(len(gold_cons))
    # Bracket test
    result.append(len(sys_cons))
    # Cross Bracket
    result.append(cross_bracket)
    
    # Words
    result.append(len(gold_tags))
    # Correct Tags
    result.append(tags_tp)
    # Tag Accuracy
    result.append(tags_tp/len(gold_tags)*100 if len(gold_tags) else 0)
    
    TOTAL_sent += 1
    TOTAL_comp_sent += (set(sys_cons) == set(gold_cons))

    if len(gold_words) <= 40:
        TOT40_match += matched_bracket
        TOT40_bn1 += len(gold_cons)
        TOT40_bn2 += len(sys_cons)
        TOT40_crossing += cross_bracket
        TOT40_no_crossing += (cross_bracket == 0)
        TOT40_2L_crossing += (cross_bracket <= 2)
        TOT40_word += len(gold_tags)
        TOT40_correct_tag += tags_tp
        TOT40_sent += 1
        TOT40_comp_sent += (set(sys_cons) == set(gold_cons))
    
    return result

# function for parsing the file
def parse_file(file_name):
    parced_data = []
    with open (file_name, "r", encoding='utf-8') as file_in:
        data = file_in.read().splitlines()
    for line in data:
        line = line.strip()
        parced_data.append(line)
    return parced_data

# main function
def main(argv):
    
    gold_file_name = os.path.join(os.getcwd(), argv[1])
    sys_file_name = os.path.join(os.getcwd(), argv[2])

    if len(argv) == 4 and argv[3] == "-evalb":
        global EVALB
        EVALB = True
    
    eval_writer = EvalFileWriter('jp-evalb.txt')
    time_start = datetime.datetime.now()
    eval_writer.write_current_time()
    eval_writer.write_header()

    parsed_gold = parse_file(gold_file_name)
    parsed_sys = parse_file(sys_file_name)

    # L = sys, R = gold
    L_trees, R_trees, L_leaves, R_leaves = extract_leaves_and_trees(parsed_sys, parsed_gold) 
    L_trees_aligned, R_trees_aligned, L_leaves_aligned, R_leaves_aligned = sentence_alignment(L_trees, R_trees, L_leaves, R_leaves)
    L_trees_merged = merging_trees(L_trees_aligned)
    R_trees_merged = merging_trees(R_trees_aligned)

    L_word_aligned, R_word_aligned = word_alignment(L_trees_merged, R_trees_merged)

    L_constituents, R_constituents, L_constituents_index_only, R_constituents_index_only \
        = get_constituents_by_reindexing(L_trees_merged, R_trees_merged, L_word_aligned, R_word_aligned)
    
    for id, (sys_words, gold_words, sys_cons, gold_cons, sys_tree, gold_tree) in enumerate(zip(L_word_aligned, R_word_aligned, L_constituents_index_only, R_constituents_index_only, L_trees_merged, R_trees_merged), 1):
        result = get_eval_result(id, sys_words, gold_words, sys_cons, gold_cons, sys_tree, gold_tree)
        eval_writer.write_eval_line(result)
    
    eval_writer.write_eval_output()
    eval_writer.write_eval_summary()

    time_end = datetime.datetime.now()

    print('START:', time_start)
    print('  END:', time_end)
    
if __name__ == "__main__":
    assert len(sys.argv) == 3 or len(sys.argv) == 4, "Usage: python jp-evalb.py gold_file_name sys_file_name"
    main(sys.argv)