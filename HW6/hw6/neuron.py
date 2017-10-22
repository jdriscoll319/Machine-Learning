import numpy
import math

class Neuron:
    def __init__(self, index, layer, step_size, num_inputs):
        #self.weights = [0.01] * (num_inputs + 1)
        self.weights = numpy.random.normal(0.0, .01, num_inputs+1)
        self.delta_weights = [0] * (num_inputs+1)
        self.output = None
        self.layer = layer
        self.error_term = None
        self.last_input = None
        self.index = index
        self.step_size = step_size

    def get_ouput(self, example):
        temp = example[:]
        temp.insert(0, 1.0)
        self.last_input = temp
        #print "weights:", self.weights
        net = numpy.dot(self.weights, temp)
        #print "net:", net
        self.output = 1 / (1 + math.exp(-1. * net))
        #print "output:", self.index, self.output

    def get_error_term(self, target_value=None, output_layer=None):
        if self.layer == 'output':
            self.error_term = self.output * (1-self.output) * (target_value-self.output)
        else:
            sum_errors = 0
            for output_node in output_layer:
                #print "summation:", sum_errors
                sum_errors += output_node.weights[self.index] * output_node.error_term
            self.error_term = self.output * (1 - self.output) * sum_errors

    def update_weights(self):
       # print "Updating weights for:", self.layer, self.index
        for index in range(0, len(self.delta_weights)):
            self.delta_weights[index] = self.step_size * self.error_term * self.last_input[index]
            #print "error term:", self.error_term
            #print "delta weights:", self.delta_weights[index]

        for index in range(0, len(self.weights)):
            self.weights[index] += self.delta_weights[index]
