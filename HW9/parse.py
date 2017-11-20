#return a list of lists.
#Each sentence(line) in dev_file is a list of each word
def parse_dev(dev_file):
    df = open(dev_file, 'r')
    dev_list = df.read().splitlines()
    df.close()
    dev_parsed = []
    for sentence in dev_list:
        dev_parsed.append(sentence.split())
    return dev_parsed

#return a list of lists
#inner list is ordered transistion probabilities
def parse_hmm_trans(trans_file):
    tf = open(trans_file, 'r')
    trans_list = tf.read().splitlines()
    tf.close()
    trans_parsed = []
    for dist in trans_list:
        temp = dist.split()
        dist_parsed = []
        for index, val in enumerate(temp):
            if index != 0:
                prob = val.split(':')
                dist_parsed.append(float(prob[1]))
        trans_parsed.append(dist_parsed) 

    return trans_parsed

#return a list of lists
#first element of inner list is the state
#second element is a dictionary with all of the emission probabilities
def parse_hmm_emit(emit_file):
    ef = open(emit_file, 'r')
    emit_list = ef.read().splitlines()
    ef.close()
    emit_parsed = []
    for dist in emit_list:
        temp = dist.split()
        dist_parsed = []
        dist_dict = {}
        for index, val in enumerate(temp):
            if index == 0:
                dist_parsed.append(val)
            else:
                prob = val.split(':')
                dist_dict[prob[0]] = float(prob[1])
        emit_parsed.append(dist_dict)  ##change to dist_parsed and uncomment below for list of list w/ dict - [ [VD, {}], ...]
        ##emit_parsed.append(dist_parsed)
    return emit_parsed

#returns a list of prior probabilities
def parse_hmm_prior(prior_file):
    pf = open(prior_file, 'r')
    prior_list = pf.read().splitlines()
    pf.close()
    prior_parsed = []
    for prior in prior_list:
        temp = prior.split()
        prior_parsed.append(float(temp[1]))
    return prior_parsed