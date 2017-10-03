import sys

inputText = open(sys.argv[1], 'r')
inputList = inputText.read()
newLineInstance = inputList.find('\n')
reversedFile = ""
while newLineInstance != -1:
    reversedFile = inputList[:newLineInstance+1] + reversedFile
    inputList = inputList[newLineInstance+1:]
    newLineInstance = inputList.find('\n')
print reversedFile

inputText.close()

