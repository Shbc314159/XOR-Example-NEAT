from Connection import Connection
from Neuron import Neuron
import globalvars 
import random
import copy 
import time

class Neural_Network():
    def __init__(self, num_inputs, num_outputs):
        self.genome_neurons = []
        self.genome_connections = []
        self.input_neurons = []
        self.output_neurons = []
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.in_out_layers()
        self.score = 0
    
    def in_out_layers(self):
        for i in range(self.num_inputs):
            neuron = Neuron(i, None, None)
            self.genome_neurons.append(neuron)
            self.input_neurons.append(neuron)
        
        for i in range(self.num_inputs, self.num_inputs + self.num_outputs):
            neuron = Neuron(i, None, None)
            self.genome_neurons.append(neuron)
            self.output_neurons.append(neuron)
        
        neuron = Neuron(self.num_inputs+self.num_outputs, None, None)
        self.genome_neurons.append(neuron)
        self.input_neurons.append(neuron)
    
    def create_connection(self, input_neuron, output_neuron):
        new_connection = True
        
        for connection in globalvars.connections:
            if connection.input_neuron == input_neuron and connection.output_neuron == output_neuron:
                new_connection = False
                innovation_number = connection.innovation_number
            
        if new_connection == True:
            innovation_number = globalvars.next_innovation_number
            globalvars.next_innovation_number += 1
            
        connection = Connection(input_neuron, output_neuron, innovation_number)
        if connection not in self.genome_connections:
            self.genome_connections.append(connection)
            globalvars.connections.append(connection)
        
        return connection
    
    def create_node(self, connection):
        input_neuron = connection.input_neuron
        output_neuron = connection.output_neuron
        new_neuron = True
        
        for neuron in globalvars.neurons:
            if neuron.input_neuron == input_neuron and neuron.output_neuron == output_neuron:
                new_neuron = False
                neuron_id = neuron.id
                
        if new_neuron == True:
            neuron_id = globalvars.next_id
            globalvars.next_id += 1
        
        connection.active = False
        neuron = Neuron(neuron_id, input_neuron, output_neuron)
        globalvars.neurons.append(neuron)
        self.genome_neurons.append(neuron)
        connection1 = self.create_connection(input_neuron, neuron.id)
        connection2 = self.create_connection(neuron.id, output_neuron)
        connection1.weight = 1
        connection2.weight = connection.weight
        
        return connection1, connection2

    def run(self, inputs):
            neuron_map = {instance.id: instance for instance in self.genome_neurons}
            self.reset()
            
            outputs = []
            active_connections = []
            
            self.input_neurons[self.num_inputs].value = 1
            
            for i in range(self.num_inputs):
                self.input_neurons[i].value = inputs[i]
                
            for connection in self.genome_connections:
                if connection.active == True:
                    active_connections.append(connection)
            
            for neuron in self.output_neurons:
                outputs.append(self.get_neuron_value(neuron.id, active_connections, neuron_map, visited=None))
            
            max_value = None
            max_index = None

            for i, value in enumerate(outputs):
                if value is not None:
                    if max_value is None or value > max_value:
                        max_value = value
                        max_index = i
            
            return outputs[0]
        
    def get_neuron_value(self, neuron_id, active_connections, neuron_map, visited):
        if visited is None:
            visited = set()

        if neuron_id in visited:
            return 0

        visited.add(neuron_id)
        
        neuron = neuron_map[neuron_id]
        for connection in active_connections:
            if connection.output_neuron == neuron_id:
                input_neuron = neuron_map[connection.input_neuron]
                if input_neuron.value == None:
                    neuron.sum += self.get_neuron_value(connection.input_neuron, active_connections, neuron_map, visited)
                else:
                    neuron.sum += input_neuron.value
        
        neuron.activate()
        
        return neuron.value
                
                
    def reset(self):
        for neuron in self.genome_neurons:
            neuron.sum = 0
            neuron.value = None
    
    def crossover(self, parent2):
        aligned_connections = []
        
        parent1_connections = self.genome_connections
        parent2_connections = parent2.genome_connections
        
        parent1_connections.sort(key=lambda x: x.innovation_number)
        parent2_connections.sort(key=lambda x: x.innovation_number)
        
        p1_index = 0
        p2_index = 0
        
        while p1_index < len(parent1_connections) and p2_index < len(parent2_connections):
            connection1 = copy.deepcopy(parent1_connections[p1_index])
            connection2 = copy.deepcopy(parent2_connections[p2_index])
            
            if connection1.innovation_number == connection2.innovation_number:
                aligned_connections.append(connection1 if random.random() < 0.5 else connection2)
                p1_index += 1
                p2_index += 1
            elif connection1.innovation_number < connection2.innovation_number:
                aligned_connections.append(connection1)
                p1_index += 1
            else:
                aligned_connections.append(connection2)
                p2_index += 1
        
        while p1_index < len(parent1_connections):
            aligned_connections.append(parent1_connections[p1_index])
            p1_index += 1
        
        while p2_index < len(parent2_connections):
            aligned_connections.append(parent2_connections[p2_index])
            p2_index += 1
        
        
        offspring = Neural_Network(self.num_inputs, self.num_outputs)
        offspring.genome_neurons = []
        offspring.input_neurons = []
        offspring.output_neurons = []
        offspring.genome_connections = aligned_connections
        offspring.in_out_layers()

        offspring_node_ids = []
        
        for neuron in offspring.genome_neurons:
            offspring_node_ids.append(neuron.id)
        
        for connection in aligned_connections:
            if connection.input_neuron not in offspring_node_ids:
                offspring_node_ids.append(connection.input_neuron)
            elif connection.output_neuron not in offspring_node_ids:
                offspring_node_ids.append(connection.output_neuron)
        
        for neuron_id in offspring_node_ids:
            for neuron in self.genome_neurons:
                if neuron.id == neuron_id:
                    new_neuron = Neuron(neuron.id, neuron.input_neuron, neuron.output_neuron)
                    if not any(new_neuron.id == neuron.id for neuron in offspring.genome_neurons):
                        offspring.genome_neurons.append(new_neuron)
            
            for neuron in parent2.genome_neurons:
                if neuron.id == neuron_id:
                    new_neuron = Neuron(neuron.id, neuron.input_neuron, neuron.output_neuron)
                    if not any(new_neuron.id == neuron.id for neuron in offspring.genome_neurons):
                        offspring.genome_neurons.append(new_neuron)
        
        return offspring

    def mutate_connection(self):
        non_output_neurons = self.genome_neurons[:self.num_inputs] + self.genome_neurons[self.num_inputs + self.num_outputs + 1:]
        input_neuron = random.choice(non_output_neurons)
        while True:
            output_neuron = random.choice(self.genome_neurons[self.num_inputs:])
            if output_neuron != input_neuron:
                break
        self.create_connection(input_neuron.id, output_neuron.id)
        
    def mutate_neuron(self):
        self.create_node(random.choice(self.genome_connections))
    
    def mutate_enable_disable(self):
        connection = random.choice(self.genome_connections)
        
        if connection.active == True:
            connection.active = False
        elif connection.active == False:
            connection.active = True
        
    def mutate_weight_shift(self):
        connection = random.choice(self.genome_connections)
        connection.weight += (random.random()/5)-0.1
        
    def mutate_weight_random(self):
        connection = random.choice(self.genome_connections)
        connection.weight = (random.random() * 4) - 2
    
    def mutate(self, probabilities):
        if probabilities[0] > random.random():
            self.mutate_connection()
            
        if probabilities[1] > random.random() and len(self.genome_connections) > 0:
            self.mutate_neuron()
            
        if probabilities[2] > random.random() and len(self.genome_connections) > 0:
            self.mutate_enable_disable()
            
        if probabilities[3] > random.random() and len(self.genome_connections) > 0:
            self.mutate_weight_shift()
        
        if probabilities[4] > random.random() and len(self.genome_connections) > 0:
            self.mutate_weight_random()
        
    def get_fitness(self, inputs, outputs):
        fitness = 0
        for i in range(len(inputs)):
            network_output = self.run(inputs[i])
            actual_output = outputs[i]
            difference = abs(actual_output[0] - network_output)
            fitness -= difference
        
        return fitness/len(inputs)
        

network = Neural_Network(2, 1)
conn1 = network.create_connection(0, 2)
conn2 = network.create_connection(1, 2)
conn3, conn4 = network.create_node(conn1)
conn5, conn6 = network.create_node(conn2)
conn7 = network.create_connection(0, 5)
conn8 = network.create_connection(1, 4)
conn9 = network.create_connection(3, 5)
conn3.weight = 1
conn4.weight = 1
conn6.weight = 1
conn5.weight = -1
conn7.weight = -1
conn8.weight = -1
conn9.weight = -1

print(network.run([0, 1]))