import sys
####################################################################
##REMOVE ME BEFORE SUBMITTING!!!!!!#################################
####################################################################
from logsum import log_sum
import parse
import math



def backward(sentence_l, prior_l, trans_ll, emit_ld):
    for sentence in sentence_l:
        beta_t=[0]*8
        sentence.reverse()
        #print alpha_a
        for index, word in enumerate(sentence):
            if index != (len(sentence) - 1):
                temp = [0] * 8
                
                for i in range(0, 8):
                    sum_beta_a_b = -1e100
                    
                    for j in range(0,8):
                        beta_a = beta_t[j] + math.log(trans_ll[i][j])
                        beta_a_b = beta_a + math.log(emit_ld[j][word])
                        sum_beta_a_b = log_sum(sum_beta_a_b, beta_a_b)
                    
                    temp[i] = sum_beta_a_b
                
                beta_t[:] = temp[:]  

        sum_beta = -1e100
        for i in range(0, 8):
            beta = math.log( prior_l[i] ) + math.log( emit_ld[i][word] ) + beta_t[i]
            sum_beta = log_sum(sum_beta, beta)
        print sum_beta

dev_l = parse.parse_dev(sys.argv[1])
hmm_trans_ll = parse.parse_hmm_trans(sys.argv[2])
hmm_emit_ld = parse.parse_hmm_emit(sys.argv[3])
hmm_prior_l = parse.parse_hmm_prior(sys.argv[4])
backward(dev_l, hmm_prior_l, hmm_trans_ll, hmm_emit_ld)
