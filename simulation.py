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