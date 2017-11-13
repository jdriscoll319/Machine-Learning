import sys
import parse
import probabilities
from math import log
from copy import deepcopy

def print_max_probabilities(max_prob_dict):
    for i in range(0,20):
        max = 0
        max_word = None

        for word in max_prob_dict:
            if max_prob_dict[word] > max:
                max = max_prob_dict[word]
                max_word = word
        
        print max_word, "%.4f" % max_prob_dict[max_word]
        del max_prob_dict[max_word]

def get_top_twenty(lib_dict, con_dict):
    lib_max_dict = {}
    con_max_dict = {}

    copy_lib_dict = deepcopy(lib_dict)
    copy_con_dict = deepcopy(con_dict)

    for i in range(0,20):
        lib_log_max = 0
        lib_max_word = None
        con_log_max = 0
        lib_max_word = None
        
        for word in copy_lib_dict:
            lib_log = log(copy_lib_dict[word] / copy_con_dict[word])
            if lib_log > lib_log_max:
                lib_log_max = lib_log
                lib_max_word = word
        lib_max_dict[lib_max_word] = lib_log_max
        del copy_lib_dict[lib_max_word]

        for word in con_dict:
            con_log = log(con_dict[word] / lib_dict[word])
            if con_log > con_log_max:
                con_log_max = con_log
                con_max_word = word
        con_max_dict[con_max_word] = con_log_max
        del con_dict[con_max_word]

    return lib_max_dict, con_max_dict

training_files = parse.parse_input_files(sys.argv[1])

##train
distinct_vocab= parse.get_distinct_vocabulary(training_files)

lib_files, con_files = parse.get_subset_files(training_files)

vocab_lib = parse.get_subset_vocab(lib_files)
vocab_con = parse.get_subset_vocab(con_files)

p_lib, p_con = probabilities.probability_outcome(training_files, lib_files)

p_word_lib = probabilities.probability_word_given_outcome(distinct_vocab, vocab_lib, 1.0)
p_word_con = probabilities.probability_word_given_outcome(distinct_vocab, vocab_con, 1.0)

lib_max_prob_dict, con_max_prob_dict = get_top_twenty(p_word_lib, p_word_con)

print_max_probabilities(lib_max_prob_dict)
print
print_max_probabilities(con_max_prob_dict)

