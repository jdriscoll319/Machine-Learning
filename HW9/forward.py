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
        alpha=[]
        alpha_a = [math.exp(-10)] * 8
        #print alpha_a
        for index, word in enumerate(sentence):
            ##calculate alpha1
            ##convert these to logsum
            if index == 0:
                for i in range(0,8):
                    alpha.append(math.log(prior_l[i]) + math.log(emit_ld[i][word]))
                #print alpha
            else:
                for i in range(0,8):
                    for j in range(0,8):
                        #print alpha_a[i], alpha[i], trans_ll[j][i]
                        alpha_a[i] = log_sum( alpha_a[i], alpha[i] + trans_ll[j][i])
                    alpha[i] = math.log(emit_ld[i][word]) + math.log(alpha_a[i])
        print math.fsum(alpha)





dev_l = parse.parse_dev(sys.argv[1])
hmm_trans_ll = parse.parse_hmm_trans(sys.argv[2])
hmm_emit_ld = parse.parse_hmm_emit(sys.argv[3])
hmm_prior_l = parse.parse_hmm_prior(sys.argv[4])
forward(dev_l, hmm_prior_l, hmm_trans_ll, hmm_emit_ld)