import Genetic_Algorithm
import cProfile
import numpy as np
import matplotlib.pyplot as plt
import math
from pynput import keyboard
import time
from multiprocessing import Pool, cpu_count, freeze_support
import simulation

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

inputs = np.random.uniform(0, 2*math.pi, 100)
inputs.sort()
inputs = [[x] for x in inputs]
outputs = []
for input1 in inputs:
    outputs.append([((np.sin(input1[0]) + 1)/2)])


def main():

    genetic_algorithm = Genetic_Algorithm.GeneticAlgorithm(1000, 0.1, 6, 4, 1.7, 1.2, 2.0, 3, 10)
    
    exit_flag = {'stop': False}
    def on_press(key):
        if key == keyboard.Key.esc:
            print("ESC pressed — will exit after current generation…")
            exit_flag['stop'] = True
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()


    genetic_algorithm.create_population()
    genetic_algorithm.run(pool)

    fitness_history = []   # will store best fitness per generation
    generations = []       # will store generation numbers

    # set up interactive plotting
    plt.ion() 
    fig, (ax_fit) = plt.subplots(1, 1, figsize=(10, 5))

    # initial empty lines
    line_fit, = ax_fit.plot([], [])
    ax_fit.set_title("Best Fitness Over Time")
    ax_fit.set_xlabel("Generation")
    ax_fit.set_ylabel("Fitness")

    plt.show()

    while genetic_algorithm.current_generation < 2000 and not exit_flag['stop']:
        gen = genetic_algorithm.current_generation
        print(f"Generation {gen}")

        # evaluate current population and record the best
        best = genetic_algorithm.best()
        fitness = best.fitness
        simulation.draw_simulation(best, genetic_algorithm.world, 2, 150)

        generations.append(gen)
        fitness_history.append(fitness)

        # --- update fitness plot ---
        line_fit.set_data(generations, fitness_history)
        ax_fit.relim()
        ax_fit.autoscale_view()

        # redraw
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)   # small pause to allow the UI to update

        print(f"→ best fitness = {fitness}")
        print(f"  Species count: {len(genetic_algorithm.species)}")

        # evolve next generation
        genetic_algorithm.create_next_generation(pool)
        genetic_algorithm.run(pool)
        genetic_algorithm.current_generation += 1
    
    genetic_algorithm.best_network.save("best_network.pkl")




if __name__ == "__main__":
    freeze_support()                  
    pool = Pool(processes=cpu_count())    
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.dump_stats("profile_data.prof")