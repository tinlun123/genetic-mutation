#!/usr/bin/env python
import abc
import math

def sigmoid(x):
    # Clamped to prevent math range erro
    if x < -500:
        x = -500
    return 1/(1 + math.exp(-x))


class NeuNet:
    """ Defines a whole meural network
        Usage:
        Create a class that extends this class, then in __init__,
        call superclass init, and then create layers with NeuNetLayer.
        It is important to note that self.first_hidden_layer must
        be set to the first hidden layer and also the order of layer
        creation should be outer layer first.
        To feed input and get an output, call start(<input list>).
        Make sure you initialize the neunet with a correct amount of
        weights.
        """

    __metaclass__ = abc.ABCMeta

    # Input layers aren't needed because they automatically feed into this.
    first_hidden_layer = None

    @abc.abstractmethod
    def __init__(self, input_size, weight_ls):
        """ Create the whole neural network here

            Go make your own!
            """
        # Increment input_size to account for bias
        input_size += 1
        self.weight_ls = weight_ls
        return

    def start(self, input_ls):
        """ Start the feed forward process with an input """
        # Append bias
        input_ls.append(1)
        return self.first_hidden_layer.feed_forward(input_ls)


class NeuNetLayer:
    """ Defines a layer of a neural network """

    def __init__(self, amount, next_layer=None, weight_ls=[], input_size=0):
        """ Create a neural network layer with the specified
            amount of neurons. If input_ls is given, give each
            neurons the input list. If next_layer is not given,
            the layer will be treated as an output layer and
            will return each neuron's value with feed_forward"""
        # Next layer is the layer to be fed forward to
        self.neurons = []
        self.next_layer = next_layer
        # Initialize neurons
        for _ in range(amount):
            neuron = Neuron(self)
            self.neurons.append(neuron)
        # Add weights to neurons
        if input_size and weight_ls:
            self.add_n_input_recurs(input_size, weight_ls)

    def feed_forward(self, input_ls=[]):
        """ Feeds the layer's inputs to the next layer's neurons
            If layer is an output layer, return the output of each
            neurons as a list """
        # Give the input layer the initial input_ls
        if input_ls:
            for neuron in self.neurons:
                neuron.inputs = input_ls
        # If is output layer
        # Returns the activation value
        if not self.next_layer:
            ret_ls = []
            for neuron in self.neurons:
                ret_ls.append(neuron.feed_forward())
                # print "{}: {}".format("input list", neuron.inputs)
            return ret_ls

        # If not output
        # Feed forward to each neurons in next layer
        for next_neuron in self.next_layer.neurons:
            next_neuron.inputs = []
            for neuron in self.neurons:
                next_neuron.inputs.append(neuron.feed_forward())
            next_neuron.inputs.append(1)  # Bias
            #print next_neuron.inputs
        return self.next_layer.feed_forward()

    def add_n_input_recurs(self, input_size, weight_ls):
        """ Add number of inputs to each neuron in this layer and then tell the next layer to do the same """
        for neuron in self.neurons:
            for _ in range(input_size):
                neuron.weights.append(weight_ls.pop())
        if self.next_layer:
            self.next_layer.add_n_input_recurs(len(self.neurons) + 1, weight_ls)


class Neuron:
    """ Defines a single neuron of a neural network """

    def __init__(self, layer):
        """ Layer defines which layer this neuron belongs to """
        self.inputs = []
        self.weights = []  # Bias is always last

    def feed_forward(self):
        """ Calculates the result and returns the activation """
        result = 0
        # print "weights: {}".format(self.weights)
        # print "inputs: {}".format(self.inputs)
        for i, w in zip(self.inputs, self.weights):
            result += i * w
        # print "result: {}".format(result)
        return self.activate(result)

    def activate(self, x):
        return sigmoid(x)
