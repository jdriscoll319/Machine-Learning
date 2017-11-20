import sys
sys.path.append('./hw9-data')
from logsum import log_sum
import parse

dev_l = parse.parse_dev(sys.argv[1])
hmm_trans_ld = parse.parse_hmm_trans(sys.argv[2])
hmm_emit_ld = parse.parse_hmm_emit(sys.argv[3])
hmm_prior_d = parse.parse_hmm_prior(sys.argv[4])
print hmm_prior_d