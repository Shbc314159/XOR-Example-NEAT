from Player import Player
from World import World
from Neural_Network import globalvars

def simulate_fitness(nn, episodes, steps_per_episode):
    total_score = 0.0
    player = Player(nn)

    for _ in range(episodes):
        World.randomise_target()
        player.reset()

        for _ in range(steps_per_episode):
            player.update()

    complexity_penalty = 1 + 0.1*(len(nn.genome.connections))
    player.fitness *= complexity_penalty
    total_score = player.fitness

    return total_score/episodes
    
def draw_simulation(nn, world, episodes, steps_per_episode):
    for _ in range(episodes):
        World.randomise_target()
        player = Player(nn)

        for _ in range(steps_per_episode):
            player.update()
            world.draw(player)

def _simulate_one(nn, episodes, steps_per_episode):
    """Simulate a single network and return its fitness."""
    player = Player(nn)
    total = 0.0
    for _ in range(episodes):
        World.randomise_target()
        player.reset()
        for _ in range(steps_per_episode):
            player.update()
        total += player.fitness
        player.fitness = 0.0

    complexity_penalty = 1 + 0.1 * len(nn.genome.connections)
    return (total / episodes) * complexity_penalty


def simulate_population_parallel(population, episodes, steps_per_episode, pool=None):
    """Simulate an entire population in parallel but avoid per-step overhead."""
    jobs = [(nn, episodes, steps_per_episode) for nn in population]
    if pool is not None:
        fitnesses = pool.starmap(_simulate_one, jobs, chunksize=1)
    else:
        fitnesses = [_simulate_one(*job) for job in jobs]

    for nn, fit in zip(population, fitnesses):
        nn.fitness = fit

    return fitnesses
