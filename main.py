import Genetic_Algorithm

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]
genetic_algorithm = Genetic_Algorithm.GeneticAlgorithm()

def main():
    
    while genetic_algorithm.current_generation < 10:
        print("Generation:", genetic_algorithm.current_generation)
        
        if genetic_algorithm.current_generation == 1:
            genetic_algorithm.create_population()
        else:
            genetic_algorithm.create_next_generation()  
            
        genetic_algorithm.run(xor_inputs, xor_outputs)  
        genetic_algorithm.current_generation += 1
    
    best_individuals = genetic_algorithm.selection()
    best_individual = best_individuals[0]
    for i in range(4):
        output = best_individual.run(xor_inputs[i])
        print(output)
    print(len(best_individual.genome_neurons))
    
    
main()