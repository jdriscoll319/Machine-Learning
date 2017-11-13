import sys
import parse
import probabilities

def print_max_probabilities(max_prob_list, max_prob_dict):
    for val in max_prob_list:
        print max_prob_dict[val], val

def get_top_twenty(lib_dict, con_dict):
    lib_max_dict = {}
    con_max_dict = {}

    for i in range(0,20):
        lib_max = 0
        lib_max_word = None
        con_max = 0
        lib_max_word = None
        
        for word in lib_dict:
            if lib_dict[word] > lib_max:
                lib_max = lib_dict[word]
                lib_max_word = word
        lib_max_dict[lib_max] = lib_max_word
        del lib_dict[lib_max_word]

        for word in con_dict:
            if con_dict[word] > con_max:
                con_max = con_dict[word]
                con_max_word = word
        con_max_dict[con_max] = con_max_word
        del con_dict[con_max_word]

    return lib_max_dict, con_max_dict

training_files = parse.parse_input_files(sys.argv[1])

##train
distinct_vocab= parse.get_distinct_vocabulary(training_files)

lib_files, con_files = parse.get_subset_files(training_files)

vocab_lib = parse.get_subset_vocab(lib_files)
vocab_con = parse.get_subset_vocab(con_files)

p_lib, p_con = probabilities.probability_outcome(training_files, lib_files)

p_word_lib = probabilities.probability_word_given_outcome(distinct_vocab, vocab_lib)
p_word_con = probabilities.probability_word_given_outcome(distinct_vocab, vocab_con)

lib_max_prob_dict, con_max_prob_dict = get_top_twenty(p_word_lib, p_word_con)

lib_vals = sorted(lib_max_prob_dict, reverse=True)
con_vals = sorted(con_max_prob_dict, reverse=True)

print_max_probabilities(lib_vals, lib_max_prob_dict)
print
print_max_probabilities(con_vals, con_max_prob_dict)

