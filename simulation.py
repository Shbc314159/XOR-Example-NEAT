from Player import Player
from World import World
from Neural_Network import globalvars

def simulate_fitness(nn, episodes=2, steps_per_episode=100):
    total_score = 0.0
    player = Player(nn)

    for _ in range(episodes):
        World.randomise_target()
        player.reset()

        for _ in range(steps_per_episode):
            player.update()

    player.fitness *= len(nn.genome.connections)
    total_score = player.fitness
    return episodes/total_score
    
def draw_simulation(nn, world, episodes=2, steps_per_episode=100):
    for _ in range(episodes):
        World.randomise_target()
        player = Player(nn)

        for _ in range(steps_per_episode):
            player.update()
            world.draw(player)