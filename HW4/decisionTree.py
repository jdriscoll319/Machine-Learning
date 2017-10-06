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

def getEntropy(attribute, data):
    num_plus = 0.
    num_minus = 0.
    total = len(data)

    for example in data:
        if example[attribute] in minus: num_minus += 1
        else: num_plus += 1

    #print total, num_plus, num_minus
    if num_minus == 0: minus_entropy = 0
    else: minus_entropy = (num_minus/total) * log((total/num_minus), 2)
    
    if num_plus == 0: plus_entropy = 0
    else: plus_entropy = (num_plus/total) * log((total/num_plus), 2)
    
    return plus_entropy + minus_entropy

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
    print "Finding Info gain for: ", candidate_attribute
    h_of_cap = getEntropy(classifier, plus_examples)
    h_of_cam = getEntropy(classifier, minus_examples)

    return h_of_c - (num_plus/total)*h_of_cap - (num_minus/total)*h_of_cam

def findBestAttr(classifier, data):
    max_gain = 0.1
    best_attr = None
    attributes = data[0].keys()
    for attribute in attributes:
        #print "Calculating attr: ", attribute
        if attribute != classifier: gain = informationGain(classifier, attribute, data)
        #print "info gain: ", gain
        if gain >= max_gain:
            max_gain = gain
            best_attr = attribute

    return best_attr

def splitData(node):
    left = []
    right = []
    for example in node.data:
        if example[node.attribute] in minus:
            del example[node.attribute]
            left.append(example)
        else:
            del example[node.attribute]
            right.append(example)
    
    return left, right

def buildTree(root, classifier, data):
    #TODO: do classification checks
    #TODO: make sure there are attributes
    root.data = data
    print "building root"
    root_attr = findBestAttr(classifier, data)
    if root_attr:
        root.attribute = root_attr
    else: return
    print "Root attribute: ", root.attribute

    root.left = Tree()
    root.right = Tree()
    root.left.data, root.right.data = splitData(root)
    #print "Left Branch data: ", root.left.data
    #print "Right Branch data: ", root.right.data

    print "Finding left branch attribute: "
    left_attr = findBestAttr(classifier, root.left.data)
    if left_attr:
        root.left.attribute = left_attr
    print "Left Branch Attribute: ", root.left.attribute

    print "finding right branch attribute"
    right_attr = findBestAttr(classifier, root.right.data)
    if right_attr:
        root.right.attribute = right_attr
    print "Right branch attribute: ", root.right.attribute

    if(not root.right.attribute and not root.left.attribute):
        return

    print "Splitting branches"
    if root.right.attribute:
        root.right.right = Tree()
        root.right.left = Tree()
        root.right.left.data, root.right.right.data = splitData(root.right)
    if root.left.attribute:
        root.left.left = Tree()
        root.left.right = Tree()
        root.left.left.data, root.left.right.data = splitData(root.left)
    
    return

def numPlusAndMinus(attribute, data):
    num_plus, num_minus = 0,0
    for example in data:
        if example[attribute] in minus:
            num_minus += 1
        else: num_plus += 1
    return num_minus, num_plus    

def printTree(root_node, classifier):
    root_minus, root_plus = numPlusAndMinus(classifier, root_node.data)
    print "[{}+/{}-]".format(root_plus, root_minus)

    if root.attribute:
        root_attr_plus = len(root.right.data)
        root_attr_minus = len(root.left.data)

    root_attribute_plus_val = root_node.data[0][root.attribute]



classifier, train_data = parseInputFile(sys.argv[1])
ID3 = Tree()

#print train_data[0]

buildTree(ID3, classifier, train_data)

print ID3.attribute
print ID3.left.attribute, ID3.right.attribute
printTree(ID3, classifier)



'''
root.data = train_data
if all_classifiers !=0 and all_classifiers !=0 and attributes exist
    root.attribute = findBestAttribute if FBA >= 0.1
        root.left.data = FBA1_minus
        root.right.data = FBA1_plus

    root.left.attribute = findBestAttribute if FBA2 >= 0.1
        root.left.left.data = FBA2_minus
        root.left.right.data = FBA2_plus

    root.right.attribute = findBestAttribute if FBA3 >= 0.1
        root.right.left.data = FBA3_minus
        root.right.right.data = FBA3_plus
'''
