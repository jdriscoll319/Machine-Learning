import sys
import parse
import probabilities
import time

start_time = time.time()

def find_top_n(num_words, vocabulary):
    vocab_dict = {}
    print num_words
    for word in vocabulary:
        if word in vocab_dict:
            vocab_dict[word] += 1
        else:
            vocab_dict[word] = 1
    
    top_n = []
    for i in range(0,num_words):
        max = 0
        max_word = None

        for word in vocab_dict:
            if vocab_dict[word] > max:
                max = vocab_dict[word]
                max_word = word

        top_n.append(max_word)
        del vocab_dict[max_word]
    
    return top_n

training_files, testing_files = parse.parse_input_files(sys.argv[1], sys.argv[2])

##train
distinct_vocab= parse.get_distinct_vocabulary(training_files)
full_vocab = parse.get_full_vocabulary(training_files)
top_words = find_top_n(int(sys.argv[3]), full_vocab)
print top_words
lib_files, con_files = parse.get_subset_files(training_files)

vocab_lib = parse.get_subset_vocab(lib_files)
vocab_con = parse.get_subset_vocab(con_files)

for word in top_words:
    distinct_vocab.remove(word)
    vocab_lib[:] = [x for x in vocab_lib if x != word]
    vocab_con[:] = [x for x in vocab_con if x != word]

p_lib, p_con = probabilities.probability_outcome(training_files, lib_files)

p_word_lib = probabilities.probability_word_given_outcome(distinct_vocab, vocab_lib)
p_word_con = probabilities.probability_word_given_outcome(distinct_vocab, vocab_con)


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
print("--- %s seconds ---" % (time.time() - start_time))
