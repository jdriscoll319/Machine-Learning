import numpy
import math

class Neuron:
    def __init__(self, index, layer, step_size, num_inputs):
        self.weights = numpy.random.normal(0.0, .04, num_inputs+1)
        self.delta_weights = [0] * (num_inputs+1)
        self.output = None
        self.layer = layer
        self.error_term = None
        self.last_input = None
        self.index = index
        self.step_size = step_size

    def get_ouput(self, example):
        example.insert(0, 1.0)
        print example
        self.last_input = example
        net = numpy.dot(self.weights, example)
        self.output = 1 / (1 + math.exp(-1. * net))

    def get_error_term(self, target_value=None, output_layer=None):
        if self.layer == 'output':
            self.error_term = self.output * (1-self.output) * (target_value-self.output)
        else:
            sum_errors = 0
            for output_node in output_layer:
                sum_errors += output_node.weights[self.index] * output_node.error_term
            self.error_term = self.output * (1 - self.output) * sum_errors

    def update_weights(self):
        for index in range(0, len(self.delta_weights)):
            self.delta_weights[index] = self.step_size * self.error_term * self.last_input[index]

        for index in range(0, len(self.weights)):
            self.weights[index] += self.delta_weights[index]
