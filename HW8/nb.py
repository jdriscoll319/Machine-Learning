import sys
import parse
import probabilities

training_files, testing_files = parse.parse_input_files(sys.argv[1], sys.argv[2])

##train
distinct_vocab_lib = parse.get_distinct_vocabulary(training_files)
distinct_vocab_con = distinct_vocab_lib

lib_files, con_files = parse.get_subset_files(training_files)

vocab_lib = parse.get_subset_vocab(lib_files)
vocab_con = parse.get_subset_vocab(con_files)

p_lib, p_con = probabilities.probability_outcome(training_files, lib_files)

p_word_lib = probabilities.probability_word_given_outcome(distinct_vocab_lib, vocab_lib)
p_word_con = probabilities.probability_word_given_outcome(distinct_vocab_con, vocab_con)

##test

#print p_word_con
