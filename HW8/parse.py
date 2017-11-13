#returns two lists of files corresponding to the list of files contained in the input arguments
def parse_input_files(arg1, arg2=None):
    #Import training examples
    input_file = open(arg1, 'r')
    training_files = input_file.read().splitlines()
    input_file.close()

    if(arg2):
        input_file = open(arg2, 'r')
        testing_files = input_file.read().splitlines()
        input_file.close()
        
        return training_files, testing_files

    return training_files

#reads the words in all of the files and returns a dictionary of distinct words with their count intialized to 1
def get_distinct_vocabulary(file_list):
    vocabulary = []
    for document in file_list:
        doc = open(document, 'r')
        vocabulary += doc.read().lower().splitlines()
        doc.close()

    distinct_vocab = set(vocabulary[:])
    return distinct_vocab

def get_full_vocabulary(file_list):
    vocabulary = []
    for document in file_list:
        doc = open(document, 'r')
        vocabulary += doc.read().lower().splitlines()
        doc.close()

    return vocabulary

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
        doc.close()
    
    return vocab

def get_test_vocab(test_doc):
    vocab = []
    doc = open(test_doc, 'r')
    vocab += doc.read().lower().splitlines()
    doc.close

    return vocab
