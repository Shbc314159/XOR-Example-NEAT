import random
import copy

class Connection():
    def __init__(self, input_neuron, output_neuron, weight, innovation_number):
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.innovation_number = innovation_number
        self.weight = weight
        self.active = True  
    
    def clone(self):
        cls = self.__class__
        new = cls.__new__(cls)
        
        new.weight = self.weight
        new.input_neuron = self.input_neuron
        new.output_neuron = self.output_neuron
        new.innovation_number = self.innovation_number
        new.active = self.active
        
        return new