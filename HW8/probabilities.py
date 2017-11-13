from math import log
#returns the probability of an outcome given the list of input files (P(liberal) and P(conservative))
def probability_outcome(file_list, lib_list):
    p_lib = float(len(lib_list))/len(file_list)
    return p_lib, 1-p_lib

#returns the probabilities of every word in a given outcome subset that word is in (P(word|outcome))
def probability_word_given_outcome(distinct_set, outcome_word_list, smoother):
    word_count = {}
    num_word_positions = len(outcome_word_list)
    num_distinct_words = len(distinct_set)

    for word in outcome_word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    probability_dict = {}
    for word in distinct_set:
        if word in word_count:
            probability_dict[word]= (word_count[word]+float(smoother))/(num_word_positions + num_distinct_words*smoother)
        else:
            probability_dict[word]= float(smoother)/(num_word_positions + num_distinct_words * smoother)

    return probability_dict

def classify_naive_bayes(distinct_set, p_word_con, p_word_lib, p_con, p_lib, word_list):
    nb_con, nb_lib = 0, 0

    for word in word_list:
        if word in distinct_set:
            nb_con += log(p_word_con[word])
            nb_lib += log(p_word_lib[word])
    
    nb_con += log(p_con)
    nb_lib += log(p_lib)

    if nb_lib > nb_con:
        return "L"
    else:
        return "C"

