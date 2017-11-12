#returns the probability of an outcome given the list of input files (P(liberal) and P(conservative))
def probability_outcome(file_list, lib_list):
    p_lib = float(len(lib_list))/len(file_list)
    return p_lib, 1-p_lib

#returns the probabilities of every word in a given outcome subset that word is in (P(word|outcome))
def probability_word_given_outcome(distinct_dict, outcome_word_list):
    for word in outcome_word_list:
        distinct_dict[word] += 1
    
    probability_dict = {}
    for word in distinct_dict:
        probability_dict[word]= float(distinct_dict[word])/(len(outcome_word_list)+len(distinct_dict))

    return probability_dict

def classify_naive_bayes(distinct_vocab_con, distinct_vocab_lib, word_list):
    nb_con, nb_lib = 0, 0

