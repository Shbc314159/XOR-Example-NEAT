import Neuron
from .Connection import Connection 
import copy
import random

class Genome:
    def __init__(self):
        self.neurons = {} 
        self.connections = {}

    def add_neuron(self, neuron_type, neuron_id):
        neuron = Neuron.Neuron(neuron_id, neuron_type)
        self.neurons[neuron_id] = neuron
        return neuron

    def add_connection(self, in_neuron, out_neuron, innovation_num, weight=None):
        if weight is None:
            weight = random.uniform(-2, 2)
        connection = Connection(in_neuron, out_neuron, weight, innovation_num)
        self.connections[innovation_num] = connection
        return connection
    
    def add_neurons_from_connections(self):
        for connection in self.connections.values():
            if connection.input_neuron not in self.neurons:
                self.add_neuron('hidden', connection.input_neuron)
            if connection.output_neuron not in self.neurons:
                self.add_neuron('hidden', connection.output_neuron)
