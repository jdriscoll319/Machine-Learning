#returns two lists of files corresponding to the list of files contained in the input arguments
def parse_input_files(arg1, arg2):
    #Import training examples
    input_file = open(arg1, 'r')
    training_files = input_file.read().splitlines()
    input_file.close()

    input_file = open(arg2, 'r')
    testing_files = input_file.read().splitlines()
    input_file.close()

    return training_files, testing_files

#reads the words in all of the files and returns a dictionary of distinct words with their count intialized to 1
def get_distinct_vocabulary(file_list):
    vocabulary = []
    for document in file_list:
        doc = open(document, 'r')
        vocabulary += doc.read().lower().splitlines()

    distinct_vocab = set(vocabulary)
    distinct_vocab = dict.fromkeys(distinct_vocab, 1)
    
    return distinct_vocab

#takes in a file list and splits into lists of liberal and conservative files
def get_subset_files(file_list):
    lib = []
    con = []
    for doc in file_list:
        if "lib" in doc:
            lib.append(doc)
        else:
            con.append(doc)
        
    return lib, con

#returns a list of every word in an outcome subset (liberal or conservative)
def get_subset_vocab(sub_list):
    vocab = []
    for document in sub_list:
        doc = open(document, 'r')
        vocab += doc.read().lower().splitlines()
    
    return vocab