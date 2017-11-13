import sys
import parse
import probabilities

training_files, testing_files = parse.parse_input_files(sys.argv[1], sys.argv[2])

##train
distinct_vocab= parse.get_distinct_vocabulary(training_files)

lib_files, con_files = parse.get_subset_files(training_files)

vocab_lib = parse.get_subset_vocab(lib_files)
vocab_con = parse.get_subset_vocab(con_files)

p_lib, p_con = probabilities.probability_outcome(training_files, lib_files)

p_word_lib = probabilities.probability_word_given_outcome(distinct_vocab, vocab_lib)
p_word_con = probabilities.probability_word_given_outcome(distinct_vocab, vocab_con)

##test
correct = 0
for doc in testing_files:
    outcome = probabilities.classify_naive_bayes(distinct_vocab, 
                                                p_word_con, p_word_lib, 
                                                p_con, p_lib, 
                                                parse.get_test_vocab(doc))
    print outcome
    if "lib" in doc and outcome == "L":
        correct += 1
    elif "con" in doc and outcome == "C":
        correct += 1


print "Accuracy: %.4f" % (float(correct)/len(testing_files))
