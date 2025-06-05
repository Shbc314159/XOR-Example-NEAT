import numpy as np

class Neuron:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.sum = 0
        self.value = None
    
    def activate(self):
        self.value = self.sigmoid(self.sum)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-4.9*x))
    
    def reset(self):
        self.sum = 0
        if self.type == 'hidden' or self.type == 'output':
            self.value = None

        if self.type == 'bias':
            self.value = 1