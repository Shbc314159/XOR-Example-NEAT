

class Species():
    def __init__(self, archetype):
        self.archetype = archetype
        self.members = [archetype] 
        self.average_fitness = 0
        self.best_fitness = float('inf') 
        self.stagnant_gens = 0
    
    def check_network(self, network, c1, c2, c3, threshold):
        genes1 = {conn.innovation_number: conn.weight for conn in self.archetype.genome.connections.values()}
        genes2 = {conn.innovation_number: conn.weight for conn in network.genome.connections.values()}

        all_gene_nums = set(genes1.keys()).union(genes2.keys())

        matching_weights = []
        disjoint = 0
        excess = 0

        max_inno1 = max(genes1.keys()) if genes1 else 0
        max_inno2 = max(genes2.keys()) if genes2 else 0
        
        for innov in all_gene_nums:
            in1 = innov in genes1
            in2 = innov in genes2
            
            if in1 and in2:
                matching_weights.append(abs(genes1[innov] - genes2[innov]))
            else:
                if innov > max_inno1 or innov > max_inno2:
                    excess += 1
                else:
                    disjoint += 1
        
        avg_weight_diff = sum(matching_weights) / len(matching_weights) if matching_weights else 0.0
        N = max(len(genes1), len(genes2), 1)
        distance = (c1 * excess / N) + (c2 * disjoint / N) + (c3 * avg_weight_diff)

        if distance < threshold:
            self.add_member(network)
            return True
        else:
            return False



    def add_member(self, member):
        self.members.append(member)
        if member.fitness < self.best_fitness:
            self.best_fitness = member.fitness
            self.archetype = member