import sys
####################################################################
##REMOVE ME BEFORE SUBMITTING!!!!!!#################################
####################################################################
sys.path.append('./hw9-data')
from logsum import log_sum
import parse
import math

def print_tagged_sentence(sentence, state_sequence):
    tagged_sentence = ""
    for index, word in enumerate(sentence):
        if index != len(sentence)-1:
            tagged_sentence += (word + '_' + state_sequence[index] + ' ')
        else:
            tagged_sentence += (word + '_' + state_sequence[index])
    print tagged_sentence
    

def viterbi(sentence_l, prior_l, trans_ll, emit_ld, pos_l):
    for sentence in sentence_l:
        ##viterbi = [[None]*10]*len(sentence)
        Q_star = [[0 for i in range(len(sentence))] for i in range(8)]
        viterbi = []
        #Q_star = []
        for index, word in enumerate(sentence):
            if index == 0:
                for i in range(0, 8):
                    #viterbi[i][index] = math.log(prior_l[i]) + math.log(emit_ld[i][word])
                    Q_star[i][index] = pos_l[i]
                    viterbi.append( math.log(prior_l[i]) + math.log(emit_ld[i][word]) )
                    #print viterbi
                    #Q_star.append(pos_l[i])

            else:
                temp_vit = [0 for x in range(8)]
                for i in range(0, 8):
                    temp = [0 for x in range(8)]
                    for j in range(0, 8):
                        temp[j] = viterbi[j] + math.log(trans_ll[j][i]) + math.log(emit_ld[i][word])
                    
                    temp_vit[i] = max(temp)
                    Q_star[i][index] = pos_l[temp.index(max(temp))]
                
                #print "temp vit: ", temp_vit
                viterbi[:] = temp_vit[:]

        max_state = viterbi.index(max(viterbi))
        #print_tagged_sentence(sentence, Q_star[max_state])
        for line in Q_star:
            print line
        return
        

dev_l = parse.parse_dev(sys.argv[1])
hmm_trans_ll = parse.parse_hmm_trans(sys.argv[2])
hmm_emit_ld = parse.parse_hmm_emit(sys.argv[3])
hmm_prior_l = parse.parse_hmm_prior(sys.argv[4])
hmm_parts_of_speech_l = parse.parse_pos(sys.argv[4])
viterbi(dev_l, hmm_prior_l, hmm_trans_ll, hmm_emit_ld,hmm_parts_of_speech_l)
