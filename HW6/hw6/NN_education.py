import sys
import numpy
import math
import parse_input
from neuron import Neuron

#Set neural net constant values.
step_size = 0.5
hidden_layer_size = 10
output_layer_size = 1

##normalize data to [0,1]
def normalize(training_examples, training_labels, dev_examples):
    for i in range(0, len(training_examples)):
        for j in range(0, len(training_examples[i])):
            training_examples[i][j] /= 100
            

        training_labels[i] /= 100
    
    for i in range(0, len(dev_examples)):
        for j in range(0, len(dev_examples[i])):
            dev_examples[i][j] /= 100

    return training_examples, training_labels, dev_examples

#create hidden layer of variable size:
def create_hidden_layer(num_neurons, input_size):
    layer = [Neuron(i, "inner", step_size, input_size) for i in range(1, num_neurons+1)]
    return layer

#create output layer of variable size
def create_output_layer(num_neurons, input_size):
    layer = [Neuron(i, "output", step_size, input_size) for i in range(1, num_neurons+1)]
    return layer

def train(training_examples, training_labels, hidden_layer, output_layer):
    error = 1
    f=open("error.txt", 'w')
    while error >= .0135:
        error = 0
        for index, example in enumerate(training_examples):
        #for index in range(0,1):
            #run examples through first layer
            #print "Example:", training_examples[index]
            hidden_output = []
            for neuron in hidden_layer:
                #neuron.get_ouput(training_examples[index])
                neuron.get_ouput(example)
                ##print "Hidden Neuron output:", neuron.output
                hidden_output.append(neuron.output)
            
            #take ouputs from first layer and input into output layer
            #get error term for output layer
            
            for neuron in output_layer:
                neuron.get_ouput(hidden_output)
                error += (training_labels[index] - neuron.output)**2
                
                #print "Output Neuron output:", neuron.output
                neuron.get_error_term(training_labels[index])
                #print "target:", training_labels[index]
                #print "error term:", neuron.error_term
                ##print "Out Neuron error:", neuron.error_term
            
            ##get error term for hidden layer
            #update weights
            
            for neuron in hidden_layer:
                neuron.get_error_term(None, output_layer)
                #print "Hidden neuron error:", neuron.error_term
                neuron.update_weights()
                ##print "Hidden neuron delta weights:", neuron.delta_weights
                ##print "Hidden neuron weights:", neuron.weights
            
            #update weights
            for neuron in output_layer:
                neuron.update_weights()
                ##print "output neuron delta weight:", neuron.delta_weights
                ##print "output neuron weights:", neuron.weights

        #print "output from last example:", output_layer[0].output
        #print "output error term:", output_layer[0].error_term
        error *= .5
        print error
        f.write(str(error))
        f.write('\n')
    f.close()



##Get all the data necessary (and maybe some stuff that's not necessary)
attributes, training_examples, training_labels, dev_examples = parse_input.parseInputFiles(sys.argv[1], sys.argv[2], sys.argv[3])
num_attributes = len(attributes)

training_examples, training_labels, dev_examples = normalize(training_examples, training_labels, dev_examples)

hidden_layer = create_hidden_layer(hidden_layer_size, num_attributes)
output_layer = create_output_layer(output_layer_size, hidden_layer_size)

train(training_examples, training_labels, hidden_layer, output_layer)

f = open("prediction.txt", 'w')
for example in dev_examples:
    #run examples through first layer
    #print "Example:", training_examples[index]
    hidden_output = []
    for neuron in hidden_layer:
        #neuron.get_ouput(training_examples[index])
        neuron.get_ouput(example)
        ##print "Hidden Neuron output:", neuron.output
        hidden_output.append(neuron.output)
    
    #take ouputs from first layer and input into output layer
    #get error term for output layer
    
    for neuron in output_layer:
        neuron.get_ouput(hidden_output)
        f.write(str(neuron.output*100))
        f.write('\n')
f.close()
