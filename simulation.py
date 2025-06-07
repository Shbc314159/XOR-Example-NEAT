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

def draw_population(population, world, episodes, steps_per_episode):
    """Draw the movements of a whole population overlaid in the same world."""
    for _ in range(episodes):
        World.randomise_target()
        players = [Player(nn) for nn in population]

        for _ in range(steps_per_episode):
            for player in players:
                player.update()
            world.draw_multi(players)


def simulate_population_parallel(population, world, episodes, steps_per_episode, pool):
    """Simulate a whole population in parallel while drawing their movements."""
    players = [Player(nn) for nn in population]

    for _ in range(episodes):
        World.randomise_target()
        for p in players:
            p.reset()

        for _ in range(steps_per_episode):
            jobs = [
                (p.brain, p.cube_pos, p.direction, p.x_center, p.z_center)
                for p in players
            ]
            moves = pool.map(_calc_move, jobs)

            for p, move in zip(players, moves):
                p.update(move)

            world.draw_multi(players)

    fitnesses = []
    for p in players:
        complexity_penalty = 1 + 0.1 * (len(p.brain.genome.connections))
        p.fitness *= complexity_penalty
        fitnesses.append(p.fitness / episodes)

    return fitnesses


def _calc_move(args):
    nn, cube_pos, direction, x_center, z_center = args
    outputs = nn.fast_run([cube_pos[0], cube_pos[1], cube_pos[2], direction, x_center, z_center])
    return outputs.index(max(outputs))
