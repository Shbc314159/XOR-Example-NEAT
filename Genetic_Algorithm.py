import neural_network
import random
import copy

class GeneticAlgorithm:
    def __init__(self):
        self.population = []
        self.current_generation = 1
        self.pop_size = 1000
        self.num_selected = 50
        self.mutation_probabilities = [0.5, 0.5, 0.5, 0.5, 0.5]
        
    
    def create_population(self):
        for i in range(self.pop_size):
            nn = neural_network.Neural_Network(2, 1)
            nn.mutate(self.mutation_probabilities)
            self.population.append(nn) 
                
    def create_next_generation(self):
        best_individuals = self.selection() 
        print(best_individuals[0].score)
        self.population = []

        for individual in best_individuals:
            individual.score = 0
    
        for i in range(self.pop_size - len(best_individuals)):
            parent1 = random.choice(best_individuals)
            parent2 = random.choice(best_individuals)
            offspring_nn = parent1.crossover(parent2)
            offspring_nn.mutate(self.mutation_probabilities)
            self.population.append(offspring_nn)
        
        for i in range(len(best_individuals)):
            parent = best_individuals[i]
            child_nn = copy.deepcopy(parent)
            self.population.append(child_nn)   
    
    def selection(self):
        selected_individuals = []
        sorted_individuals = sorted(self.population, key=lambda x: x.score, reverse=True)
        selected_individuals = sorted_individuals[:self.num_selected]   
        return selected_individuals     
    
    def run(self, inputs, outputs):
        for neural_network in self.population:
            neural_network.score = neural_network.get_fitness(inputs, outputs)