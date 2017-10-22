import csv

def parseInputFiles(arg1, arg2, arg3):
    #Import training examples
    input_file = open(arg1, 'r')
    reader = csv.reader(input_file, skipinitialspace=True)

    training_examples= []
    first_row = True
    for row in reader:
        example = []
        if first_row: 
            training_examples.append(row)
            first_row = False
        else:
            for val in row:
                if val == 'yes':
                    example.append(1.0)
                elif val == 'no':
                    example.append(0.0)
                else: example.append(float(val))
            training_examples.append(example)

    attributesWS = training_examples[0]
    attributes = []
    #remove whitespace to be safe
    for a in attributesWS:
        b = a.replace(" ", "")
        attributes.append(b)

    training_examples= training_examples[1:]
    input_file.close()

    ##############################
    #Import training example labels
    input_file = open(arg2, 'r')
    training_label_data = input_file.read().splitlines()

    training_labels = []
    for val in training_label_data:
        if val == 'yes':
            training_labels.append(1.0)
        elif val == 'no':
            training_labels.append(0.0)
        else: training_labels.append(float(val))


    ##############################
    #Import development set
    input_file = open(arg3, 'r')
    reader = csv.reader(input_file, skipinitialspace=True)

    dev_examples = []
    next(reader, None)
    for row in reader:
        example = []
        for val in row:
            if val == 'yes':
                example.append(1.0)
            elif val == 'no':
                example.append(0.0)
            else: example.append(float(val))
        dev_examples.append(example)

    input_file.close()

    return attributes, training_examples, training_labels, dev_examples
