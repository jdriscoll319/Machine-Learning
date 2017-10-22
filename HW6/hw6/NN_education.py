import sys
import numpy
import math
import parse_input
from neuron import Neuron

#Set neural net constant values.
step_size = 0.1
hidden_layer_size = 2
output_layer_size = 1

#create hidden layer of variable size:
def create_hidden_layer(num_neurons, input_size):
    layer = [Neuron(i, "inner", step_size, input_size) for i in range(1, num_neurons+1)]
    return layer

#create output layer of variable size
def create_output_layer(num_neurons, input_size):
    layer = [Neuron(i, "outer", step_size, input_size) for i in range(1, num_neurons+1)]
    return layer



##Get all the data necessary (and maybe some stuff that's not necessary)
attributes, training_examples, training_labels, dev_examples = parse_input.parseInputFiles(sys.argv[1], sys.argv[2], sys.argv[3])
num_attributes = len(attributes)

#create the two layers
hidden_layer = create_hidden_layer(hidden_layer_size, num_attributes)
output_layer = create_output_layer(output_layer_size, hidden_layer_size)
for neuron in hidden_layer:
    print neuron.weights
hidden_output = []
for index, example in enumerate(training_examples):
    #run examples through first layer
    for neuron in hidden_layer:
        print neuron.index
        neuron.get_ouput(example)
        hidden_output.append(neuron.output)
    
    #take ouputs from first layer and input into output layer
    #get error term for output layer
    for neuron in output_layer:
        neuron.get_ouput(hidden_output)
        neuron.get_error_term(training_labels[index])
    
    ##get error term for hidden layer
    #update weights
    for neuron in hidden_layer:
        neuron.get_error_term(None, output_layer)
        neuron.update_weights
    
    #update weights
    for neuron in output_layer:
        neuron.update_weights

##print output_layer[0].output
    
    

    