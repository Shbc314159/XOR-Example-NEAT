import random

class Connection:
    def __init__(self, input_neuron, output_neuron, innovation_number):
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.active = True
        self.innovation_number = innovation_number
        self.weight = random.random()