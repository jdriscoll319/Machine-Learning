import sys
####################################################################
##REMOVE ME BEFORE SUBMITTING!!!!!!#################################
####################################################################
sys.path.append('./hw9-data')
from logsum import log_sum
import parse
import math



def forward(sentence_l, prior_l, trans_ll, emit_ld):
    for sentence in sentence_l:
        alpha_t=[]
        
        #print alpha_a
        for index, word in enumerate(sentence):
            ##calculate alpha1
            ##convert these to logsum
            if index == 0:
                print "FIRST WORD:"
                for i in range(0,8):
                    #print prior_l[i], emit_ld[i][word]
                    ##alpha_t.append( math.log(prior_l[i]) + math.log(emit_ld[i][word]) )
                    alpha_t.append( prior_l[i] * emit_ld[i][word] )
                print alpha_t
                print
            else:
                print "WORD" , index
                temp = [0]*8
                for i in range(0,8):
                    print"  Alpha( state =" , i , ")"
                    sum_alpha_a = math.exp(-100)
                    
                    for j in range(0,8):
                        #print alpha_a[i], alpha[i], trans_ll[j][i]
                        alpha_a = alpha_t[j] * trans_ll[j][i]
                        print "    Alpha*a =", alpha_a
                        sum_alpha_a = log_sum(math.log(sum_alpha_a), math.log(alpha_a))
                        print "    Summation:" , sum_alpha_a
                    temp[i] = math.log(emit_ld[i][word]) + sum_alpha_a
                    print "    Final Summation:" , temp[i]
                alpha_t[:] = temp[:]
                print "  Alpha( t=" , index , ")", alpha_t
        print math.fsum(alpha_t)
        return 
        

dev_l = parse.parse_dev(sys.argv[1])
hmm_trans_ll = parse.parse_hmm_trans(sys.argv[2])
hmm_emit_ld = parse.parse_hmm_emit(sys.argv[3])
hmm_prior_l = parse.parse_hmm_prior(sys.argv[4])
forward(dev_l, hmm_prior_l, hmm_trans_ll, hmm_emit_ld)
