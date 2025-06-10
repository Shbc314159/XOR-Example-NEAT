import random
import sys
sys.path.append('C:/Users/samue/OneDrive/Desktop/NEAT/')
from Neural_Network import Neural_Network as network
import copy
from Species import Species
from multiprocessing import Pool, cpu_count
import math
from World import World
import simulation

class GeneticAlgorithm:    
    try:
        from line_profiler import profile
    except ImportError:
        def profile(func):
            return func
    def __init__(self, size, selection_percent, num_inputs, num_outputs,
                 c1, c2, c3, threshold, target_species,
                 stagnation_limit=10):
        # Population parameters
        self.pop_size = size
        self.percent_selected = selection_percent
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        # Speciation parameters
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.threshold = threshold
        self.target_species = target_species

        self.stagnation_limit = stagnation_limit

        # Global best tracking
        self.best_fitness_ever = float('inf')
        self.best_network = None
        self.gens_since_improvement = 0

        # GA state
        self.population = []
        self.current_generation = 1
        self.species = []

        self.world = World()

    def create_population(self):
        for _ in range(self.pop_size):
            nn = network.Neural_Network(self.num_inputs, self.num_outputs, 0.05, 0.1, 0.5)
            nn.mutate()
            self.population.append(nn)

    @profile
    def create_next_generation(self, pool):
        best_fitness = self.best().fitness

        self.speciate()

        epsilon = 1e-6
        species_scores = {}
        total_score = 0.0
        for sp in self.species:
            # keep only the top individuals of each species
            num_top = max(int(self.percent_selected * len(sp.members)), 1)
            sp.members.sort(key=lambda m: m.fitness)
            sp.members = sp.members[:num_top]

            # compute adjusted fitness in the NEAT sense
            size = len(sp.members)
            score = 0.0
            for member in sp.members:
                score += (1.0 / (member.fitness + epsilon)) / size

            species_scores[sp] = score
            total_score += score

        num_offspring = self.pop_size - len(self.species)
        expected = {sp: (species_scores[sp] / total_score) * num_offspring for sp in self.species}

        kids_per_sp = {}
        for sp, exp in expected.items():
            kids_per_sp[sp] = max(1, int(math.floor(exp)))

        allocated = sum(kids_per_sp.values())

        remainders = sorted(
            ((expected[sp] - kids_per_sp[sp], sp) for sp in self.species),
            key=lambda t: t[0],
            reverse=True,
        )
        if allocated < num_offspring:
            for i in range(num_offspring - allocated):
                kids_per_sp[remainders[i % len(remainders)][1]] += 1
        elif allocated > num_offspring:
            over = allocated - num_offspring
            removable = sorted(
                ((kids_per_sp[sp] - expected[sp], sp) for sp in self.species),
                key=lambda t: t[0],
                reverse=True,
            )
            idx = 0
            while over > 0 and removable:
                sp = removable[idx % len(removable)][1]
                if kids_per_sp[sp] > 1:
                    kids_per_sp[sp] -= 1
                    over -= 1
                idx += 1

        pairings = []
        for sp, n_kids in kids_per_sp.items():
            for _ in range(n_kids):
                p1 = random.choice(sp.members)
                p2 = random.choice(sp.members)
                pairings.append((p1, p2))

        children = pool.starmap(GeneticAlgorithm._make_child, pairings)

        new_population = []
        new_population.extend(children[: self.pop_size - len(self.species)])
        for species in self.species:
            best = species.members[0]
            new_population.append(best)
        
        if self.best_network:
            new_population.append(self.best_network)

        # reset fitness & rebuild flags (they’re already rebuilt, but clear fitness)
        for ind in new_population:
            ind.fitness = 0.0

        self.population = new_population

        if best_fitness < self.best_fitness_ever:
            self.best_fitness_ever = best_fitness
            self.gens_since_improvement = 0
        else:
            self.gens_since_improvement += 1

        if self.gens_since_improvement > self.stagnation_limit:
            print("Stagnation detected, injecting randomness")
            self._inject_randomness()
            self.gens_since_improvement = 0

    def best(self):
        self.best_network = min(self.population, key=lambda x: x.fitness)
        return self.best_network
    
    @staticmethod
    def _make_child(p1, p2):
        child = p1.crossover(p2)
        child.setup() 
        child.mutate()
        child.rebuild = True  

        return child

    def run(self, pool):

        #jobs = [(nn,) for nn in self.population]
        #results = []
        #for nn in self.population:
           # results.append(GeneticAlgorithm._compute_fitness(nn))
        #results = pool.starmap(GeneticAlgorithm._compute_fitness, jobs, chunksize=10)
        results = simulation.simulate_population_parallel(self.population, 2, 100, pool)

        for nn, fit in zip(self.population, results):
            nn.fitness = fit

    @staticmethod
    def _compute_fitness(nn):
        from simulation import simulate_fitness
        
        return simulate_fitness(nn, 2, 100)

    def speciate(self):
        for sp in self.species:
            sp.members = []

        for ind in self.population:
            assigned = False
            for sp in self.species:
                if sp.check_network(ind, self.c1, self.c2, self.c3, self.threshold):
                    assigned = True
                    break
            if not assigned:
                new_sp = Species(ind)
                new_sp.best_fitness = ind.fitness
                new_sp.stagnant_gens = 0
                self.species.append(new_sp)
                print('New species created!')


        survivors = []
        for sp in self.species:
            if not sp.members:
                print('Removing species with fitness ', sp.best_fitness)
                continue
            sp.members.sort(key=lambda x: x.fitness)
            curr_best = sp.members[0].fitness
            if curr_best < getattr(sp, 'best_fitness', float('inf')):
                sp.best_fitness = curr_best
                sp.stagnant_gens = 0
            else:
                sp.stagnant_gens += 1
            if sp.stagnant_gens < 15 or sp.best_fitness < 1.05 * self.best_fitness_ever:
                survivors.append(sp)
                
        self.species = survivors

        self.threshold += (len(self.species) - self.target_species) * 0.05
        self.threshold = max(0.7, min(self.threshold, 4.0))
        print('Threshold: ', self.threshold)

    def _inject_randomness(self, num=10):
        """Replace a portion of the worst individuals with fresh networks."""
        n_replace = num
        self.population.sort(key=lambda n: n.fitness, reverse=True)
        for i in range(n_replace):
            nn = network.Neural_Network(self.num_inputs, self.num_outputs, 0.05, 0.1, 0.5)
            nn.mutate()
            self.population[-(i+1)] = nn
 