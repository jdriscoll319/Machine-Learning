import sys
import csv
from math import log

plus = {"y", "yes", "A", "democrat", "before1950", "morethan3min", "fast", "expensive", "high", "Two", "large"}
minus = {"n", "no", "notA", "republican", "after1950", "lessthan3min", "slow", "cheap", "low", "MoreThanTwo", "small"}

class Tree:
    def __init__(self):
        self.attribute = None
        self.data = None
        self.left = None
        self.right = None

def parseInputFile(arg):
    inputFile = open(arg, 'r')
    data = []
    reader = csv.reader(inputFile, skipinitialspace=True)

    for row in reader:
        example = [row]
        data += example
    inputFile.close()

    attributesWS = data[0]
    attributes = []
    #remove whitespace to be safe
    for a in attributesWS:
        b = a.replace(" ", "")
        attributes.append(b)

    classifier = attributes[len(attributes)-1]

    #Create list of dictionaries key = attribute, value = attribute value
    listdict = []
    for example in data[1:]:
        tmpdict = {}
        for i, attr in enumerate(attributes):
            tmpdict[attr] = example[i]
        listdict.append(tmpdict)

    return classifier, listdict

def emptyTree():
    root = Tree()
    root.left = Tree()
    root.right = Tree()

    return root

def getEntropy(attribute, data):
    num_plus = 0.
    num_minus = 0.
    total = len(data)

    for example in data:
        if example[attribute] in minus: num_minus += 1
        else: num_plus += 1

    print total, num_plus, num_minus
    return ((num_plus/total) * log((total/num_plus), 2)) + ((num_minus/total) * log((total/num_minus), 2))

#assume that I'm going to filtering the lists elsewhere in the code so this will be given only the data it should be looking at,
#no need to check to see if it contains data that should calculate on
def informationGain(classifier, candidate_attribute, data):
    h_of_c = getEntropy(classifier, data)
    num_plus = 0.
    num_minus = 0.
    total = len(data)

    plus_examples = []
    minus_examples = []

    for example in data:
        if example[candidate_attribute] in minus:
            num_minus += 1
            minus_examples.append(example)
        else:
            num_plus += 1
            plus_examples.append(example)

    h_of_cap = getEntropy(classifier, plus_examples)
    h_of_cam = getEntropy(classifier, minus_examples)

    return h_of_c - (num_plus/total)*h_of_cap - (num_minus/total)*h_of_cam

def findBestAttr(classifier, data):
    max_gain = 0.1
    best_attr = None
    attributes = data[0].keys()
    for attribute in attributes:
        print "Calculating attr: ", attribute
        if attribute != classifier: gain = informationGain(classifier, attribute, data)
        print "info gain: ", gain
        if gain > max_gain:
            max_gain = gain
            best_attr = attribute

    return best_attr, max_gain

classifier, train_data = parseInputFile(sys.argv[1])
#print train_data[0]
print findBestAttr(classifier, train_data)