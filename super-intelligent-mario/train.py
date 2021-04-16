from __init__ import PROJ_DIR

# this is the absolute path to the `PROJ_DIR` directory, obtained from the __init__.py in this package
import neat
import pickle
import retro
import os
import numpy as np

# from utils.rominfo import *
# from utils.utils import *

######## MODDELING ########
# In Super Mario World-Snes,
# each button press is represented by one bit.
# So, we can represent an action of the agent as an array of 12 bits
# [0,0,0,0,0,0,0,0,0,0,0,0]
#
# But not all buttons pressess perform meaninful actions and some are redundant (start, select, R,  L, x and y)
# Below is a list of the interesting buttons and their representation as an array of bits
# jump          [1,0,0,0,0,0,0,0,0,0,0,0]
# run modifier  [0,1,0,0,0,0,0,0,0,0,0,0] (there is another button for running, but only one is needed)
# up            [0,0,0,0,1,0,0,0,0,0,0,0]
# down          [0,0,0,0,0,1,0,0,0,0,0,0]
# left          [0,0,0,0,0,0,1,0,0,0,0,0]
# right         [0,0,0,0,0,0,0,1,0,0,0,0]
# spin jump     [0,0,0,0,0,0,0,0,1,0,0,0]
#
# The agent can press multiple buttons at a time and we can better represent what actions the agent might take like this
# [x,x,0,0,x,x,x,x,x,0,0,0]
# where x is either 0 or 1 and some regions are always zero (the not interesting or redundant buttons)


# x_pos = 4830 is roughly the end of level


def report_progess(genome_id, action, info, reward, fitness, frame, last_frame_progress):
    action = [int(a) for a in action]  # reformatting action for better visualization

    print(
        genome_id,
        action,
        info,
        " reward: {:.2f}".format(reward),
        " fitness: {:.2f}".format(fitness),
        " frames w/o progess {:d}".format(frame - last_frame_progress),
    )
    return


# auxiliary function to eval_genomes for evaluating a single genome
def eval_genome(env, genome_id, genome, config):
    obs = env.reset()  # reset env to starting state

    # Altough it is an old SNES game, Super Mario's resolution is unnecessarily high and can impact performance
    # Therefore, we can reduce this resolution by a factor of 8 for each dimension without much loss of quality
    # this is the setup for reducing the resolution
    iny, inx, inc = env.observation_space.shape
    iny = int(iny / 8)
    inx = int(inx / 8)

    # create a neural network for the genome
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Simulate a game, let this genome play it and evaluate its fitness
    done = False
    fitness = 0.0

    last_distance = 0
    last_frame_progress = 0
    frame = 0
    while not done:
        # resize SNES otuput resolution and convert it to a 1d array
        obs = obs[:, :, 0]
        obs = np.resize(obs, (inx, iny))
        screen = obs.flatten()

        # feed the network the current SNES screen. Its output is an action we can input into the emulator
        action = net.activate(screen)
        # feed the emulator with the networks output and collect stats provided by Retro
        # info are the interesting variables the game provides and is defined in the data.json
        # reward and done policy is defined in scenario.json
        obs, reward, done, info = env.step(action)

        # optional - renders the screen so we can follow progess
        # env.render()

        # fitness is simply the sum of all rewards
        fitness += reward

        # if the agent is inactive or is going backwards for too long, kill it
        frame += 1
        if info["distance"] > last_distance:
            last_frame_progress = frame

        if frame - last_frame_progress >= 1000:
            done = True

        # if frame % 100 == 0:
        # report_progess(genome_id, action, info, reward, fitness, frame, last_frame_progress)

        # store current distance for next iteration
        last_distance = info["distance"]
    return fitness


# this funcion is used by Neat's run function to determine each individual's fitness
def eval_genomes(genomes, config):
    # Initialize a game at YoshiIsland2
    # data.json contains interesting in-game variables and their memory addresses
    # scenario.json specifies the done condition and the reward system
    # if not specified, retro uses its default files
    env = retro.make(
        game="SuperMarioWorld-Snes",
        scenario=os.path.join(PROJ_DIR, "cfg/custom_scenario.json"),
        info=os.path.join(PROJ_DIR, "cfg/custom_data.json"),
        state="YoshiIsland2",
        players=1,
        record=os.path.join(PROJ_DIR, "recordings"),
    )

    # For every individual in the population, evaluate it's fitness
    for genome_id, genome in genomes:
        # print("Evaluating genome {:d}".format(genome_id))
        genome.fitness = eval_genome(env, genome_id, genome, config)


def train():
    print("Training starting")

    # Set up neat's config and create a population
    # using default values and custom parameters in `cfg/neat-config`
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        os.path.join(PROJ_DIR, "cfg/neat-config"),
    )
    p = neat.Population(config)

    # Neat has a nice terminal reporting features
    # it also creates checkpoints we can come back to afterwards
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    # run until an agent wins the game
    winner = p.run(eval_genomes)