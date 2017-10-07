import sys
import csv
from math import log
from copy import deepcopy

plus = {"y", "yes", "A", "democrat", "before1950", "morethan3min", "fast", "expensive", "high", "Two", "large"}
minus = {"n", "no", "notA", "republican", "after1950", "lessthan3min", "slow", "cheap", "low", "MoreThanTwo", "small"}

class Tree:
    def __init__(self):
        self.attribute = None
        self.label = None
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
        if attribute != classifier: 
            gain = informationGain(classifier, attribute, data)
            print "info gain: ", gain
            if gain >= max_gain:
                max_gain = gain
                best_attr = attribute

    return best_attr

def splitData(node):
    left = []
    right = []
    for example in node.data:
        if example[node.attribute] in minus:
            left.append(deepcopy(example))
            del left[-1][node.attribute]
        else:
            right.append(deepcopy(example))
            del right[-1][node.attribute]
    
    return left, right

def numPlusAndMinus(attribute, data):
    num_plus, num_minus = 0,0
    for example in data:
        if example[attribute] in minus:
            num_minus += 1
        else: num_plus += 1
    return num_minus, num_plus    

def getAttributeValues(attribute, data):
    attr_plus_val, attr_minus_val = '', ''
    i = 0
    while (len(attr_minus_val) == 0 or len(attr_plus_val) == 0) and i<len(data):
        if data[i][attribute] in minus:
            attr_minus_val = data[i][attribute]
        elif data[i][attribute] in plus:
            attr_plus_val = data[i][attribute]
        i += 1
        
    return attr_minus_val, attr_plus_val

def buildTree(root, classifier, data):
    root.data = data
    
    #determine what the positive and negative labels are
    classifier_minus_val, classifier_plus_val = getAttributeValues(classifier, data)

    #Check to see if all positive or negative labels
    minus_classifiers, plus_classifiers = numPlusAndMinus(classifier, data)
    if plus_classifiers == 0:
        root.label = classifier_minus_val
        return
    elif minus_classifiers == 0:
        root.label = classifier_plus_val
        return
    
    #label root node with most common classifier
    if plus_classifiers > minus_classifiers:
        root.label = classifier_plus_val
    else:
        root.label = classifier_minus_val

    #make sure we have actual attributes
    if len(data[0]) == 1:
        return

    #Find best attribute to split the root node on
    print "building root"
    root_attr = findBestAttr(classifier, data)
    if root_attr:
        root.attribute = root_attr
    else: return
    print "Root attribute: ", root.attribute

    #Build root branches, label them with their most common classifiers
    root.left = Tree()
    root.right = Tree()
    root.left.data, root.right.data = splitData(root)
    right_minus_classifiers, right_plus_classifiers = numPlusAndMinus(classifier, root.right.data)
    left_minus_classifiers, left_plus_classifiers = numPlusAndMinus(classifier, root.left.data)

    if right_minus_classifiers > right_plus_classifiers:
        root.right.label = classifier_minus_val
    else: root.right.label = classifier_plus_val

    if left_minus_classifiers > left_plus_classifiers:
        root.left.label = classifier_minus_val
    else: root.left.label = classifier_plus_val

    #Find best attribute to split left branch on
    print "Finding left branch attribute: "
    left_attr = findBestAttr(classifier, root.left.data)
    if left_attr:
        root.left.attribute = left_attr
    print "Left Branch Attribute: ", root.left.attribute

    #Find best attribute to split right branch on
    print "finding right branch attribute"
    right_attr = findBestAttr(classifier, root.right.data)
    if right_attr:
        root.right.attribute = right_attr
    print "Right branch attribute: ", root.right.attribute

    #If we couldn't split either branch we're done
    if(not root.right.attribute and not root.left.attribute):
        return

    #Build leaf nodes and label them
    print "Splitting branches"
    if root.right.attribute:
        root.right.right = Tree()
        root.right.left = Tree()
        root.right.left.data, root.right.right.data = splitData(root.right)
        
        right_right_minus_classifiers, right_right_plus_classifiers = numPlusAndMinus(classifier, root.right.right.data)
        right_left_minus_classifiers, right_left_plus_classifiers = numPlusAndMinus(classifier, root.right.left.data)

        if right_right_minus_classifiers > right_right_plus_classifiers:
            root.right.right.label = classifier_minus_val
        else: root.right.right.label = classifier_plus_val

        if right_left_minus_classifiers > right_left_plus_classifiers:
            root.right.left.label = classifier_minus_val
        else: root.right.left.label = classifier_plus_val

    if root.left.attribute:
        root.left.left = Tree()
        root.left.right = Tree()
        root.left.left.data, root.left.right.data = splitData(root.left)

        left_right_minus_classifiers, left_right_plus_classifiers = numPlusAndMinus(classifier, root.left.right.data)
        left_left_minus_classifiers, left_left_plus_classifiers = numPlusAndMinus(classifier, root.left.left.data)

        if left_right_minus_classifiers > left_right_plus_classifiers:
            root.left.right.label = classifier_minus_val
        else: root.left.right.label = classifier_plus_val

        if left_left_minus_classifiers > left_left_plus_classifiers:
            root.left.left.label = classifier_minus_val
        else: root.left.left.label = classifier_plus_val
    
    return

def printTree(root_node, classifier):
    root_minus, root_plus = numPlusAndMinus(classifier, root_node.data)
    print "[{}+/{}-]".format(root_plus, root_minus)

    if root_node.attribute:
        root_attr_minus_val, root_attr_plus_val = getAttributeValues(root_node.attribute, root_node.data)
        root_right_minus, root_right_plus = numPlusAndMinus(classifier, root_node.right.data)
        root_left_minus, root_left_plus = numPlusAndMinus(classifier, root_node.left.data)    
        print  "{} = {}: [{}+/{}-]".format(root_node.attribute, root_attr_plus_val, root_right_plus, root_right_minus)
        if root_node.right.attribute:
            right_attr_minus_val, right_attr_plus_val = getAttributeValues(root_node.right.attribute, root_node.data)
            right_right_minus, right_right_plus = numPlusAndMinus(classifier, root_node.right.right.data)
            right_left_minus, right_left_plus = numPlusAndMinus(classifier, root_node.right.left.data)
            print  "| {} = {}: [{}+/{}-]".format(root_node.right.attribute, right_attr_plus_val, right_right_plus, right_right_minus)
            print  "| {} = {}: [{}+/{}-]".format(root_node.right.attribute, right_attr_minus_val, right_left_plus, right_left_minus)
        
        print  "{} = {}: [{}+/{}-]".format(root_node.attribute, root_attr_minus_val, root_left_plus, root_left_minus)
        if root_node.left.attribute:
            left_attr_minus_val, left_attr_plus_val = getAttributeValues(root_node.left.attribute, root_node.data)
            left_right_minus, left_right_plus = numPlusAndMinus(classifier, root_node.left.right.data)
            left_left_minus, left_left_plus = numPlusAndMinus(classifier, root_node.left.left.data)
            print  "| {} = {}: [{}+/{}-]".format(root_node.left.attribute, left_attr_plus_val, left_right_plus, left_right_minus)
            print  "| {} = {}: [{}+/{}-]".format(root_node.left.attribute, left_attr_minus_val, left_left_plus, left_left_minus)
        
def getTrainingError(root, classifier):
    total = len(root.data)
    leaf_sum = 0.
    minus, plus = 0., 0.

    if not root.attribute:
        minus, plus = numPlusAndMinus(classifier, root.data)
        return min(minus/total, plus/total)

    if not root.right.attribute:
        minus, plus = numPlusAndMinus(classifier, root.right.data)
        leaf_sum += min(minus, plus)
    else:
        #right left
        minus, plus = numPlusAndMinus(classifier, root.right.left.data)
        leaf_sum += min(minus, plus)
        #right right
        minus, plus = numPlusAndMinus(classifier, root.right.right.data)
        leaf_sum += min(minus, plus)

    if not root.left.attribute:
        minus, plus = numPlusAndMinus(classifier, root.left.data)
        leaf_sum += min(minus, plus)
    else:
        #left left
        minus, plus = numPlusAndMinus(classifier, root.left.left.data)
        leaf_sum += min(minus, plus)
        #left right
        minus, plus = numPlusAndMinus(classifier, root.left.right.data)
        leaf_sum += min(minus, plus)

    return leaf_sum/total

classifier, train_data = parseInputFile(sys.argv[1])
ID3 = Tree()

#print train_data[0]

buildTree(ID3, classifier, train_data)

print ID3.attribute
print ID3.left.attribute, ID3.right.attribute
printTree(ID3, classifier)
print "error(train): ", getTrainingError(ID3, classifier)

