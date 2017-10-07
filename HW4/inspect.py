import sys
import csv
from math import log

def readInputFile(arg):
    inputFile = open(arg, 'r')
    data = []
    reader = csv.reader(inputFile)
    for row in reader:
        example = [row]
        data += example
    inputFile.close()
    return data


#returns a list of just class converted to [0,1]
#[republican, demo]
#[notA, A]
#[no, yes]
def getClass(trainData):
    classList = []
    trainData = trainData[1:]
    for example in trainData:
        if example[len(example)-1] in {"republican", "notA", "no"}:
            classList.append(0)
        else: classList.append(1)

    return classList

def getEntropyandError(classList):
    numOne = 0.
    numZero = 0.
    total = len(classList)

    for i in classList:
        if i == 0:
            numZero += 1
        else: numOne += 1
    entropy = ((numOne/total) * log((total/numOne), 2)) + ((numZero/total) * log((total/numZero), 2))
    error = min(numOne/total, numZero/total)
    return entropy, error


trainData = readInputFile(sys.argv[1])
classList = getClass(trainData)
entropy, error = getEntropyandError(classList)
print "entropy:", entropy
print "error:", error
