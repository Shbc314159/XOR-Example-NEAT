import numpy as np

class Neuron:
    def __init__(self, id, input_neuron, output_neuron):
        self.id = id
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.sum = 0
        self.value = None
        self.activation_functions = [self.tanh, self.sigmoid, self.relu]
        self.chosen_function = np.random.choice(self.activation_functions)
    
    def activate(self):
        self.sum = self.clip(self.sum, -20, 20)
        self.value = self.chosen_function(self.sum)

    def sigmoid(self, x):
        return 1 / (1 + np.e**-x)

    def tanh(self, x):
        return np.tanh(x)

    def relu(self, x):
        return np.maximum(0, x)

    def clip(self, value, min_value, max_value):
        if value < min_value:
            return min_value
        elif value > max_value:
            return max_value
        else:
            return value

    