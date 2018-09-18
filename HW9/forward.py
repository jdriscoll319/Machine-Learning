import sys
####################################################################
##REMOVE ME BEFORE SUBMITTING!!!!!!#################################
####################################################################
from logsum import log_sum
import parse
import math



def forward(sentence_l, prior_l, trans_ll, emit_ld):
    for sentence in sentence_l:
        alpha_t=[]
        
        #print alpha_a
        for index, word in enumerate(sentence):
            ##calculate alpha1
            if index == 0:
                for i in range(0,8):
                    alpha_t.append( math.log(prior_l[i]) + math.log( emit_ld[i][word] ) )
            
            #calculate rest of the sentence
            else:
                temp = [0]*8
                for i in range(0,8):
                    sum_alpha_a = -1e100
                    
                    for j in range(0,8):
                        alpha_a = alpha_t[j] + math.log( trans_ll[j][i] )
                        sum_alpha_a = log_sum( sum_alpha_a, alpha_a )
                    
                    temp[i] = math.log(emit_ld[i][word]) + sum_alpha_a
                
                alpha_t[:] = temp[:]
        
        sum_alpha = -1e100
        for i in range(0, 8):
            sum_alpha = log_sum(sum_alpha, alpha_t[i])
        print sum_alpha
         
        

dev_l = parse.parse_dev(sys.argv[1])
hmm_trans_ll = parse.parse_hmm_trans(sys.argv[2])
hmm_emit_ld = parse.parse_hmm_emit(sys.argv[3])
hmm_prior_l = parse.parse_hmm_prior(sys.argv[4])
forward(dev_l, hmm_prior_l, hmm_trans_ll, hmm_emit_ld)
