from . import PROJ_DIR # absolute path to this project's directory
from core.custom_reporting import CustomStdOutReporter
from core.rominfo import *

import neat
import pickle
import retro
import os
import sys
import pathlib
import numpy as np
from time import sleep
from multiprocessing import cpu_count
from neat.parallel import *
from gym.envs.classic_control import rendering


"""
In Super Mario World-Snes,
each button press is represented by one bit.
So, we can represent an action of the agent as an array of 12 bits - And that is what gym-retro does
[0,0,0,0,0,0,0,0,0,0,0,0]

But not all buttons pressess perform meaninful actions and some are redundant. start, select, R,  L and up are useless. x and y are redundant
Below is a list of the interesting buttons and their representation as an array of bits
jump          [1,0,0,0,0,0,0,0,0,0,0,0]
run modifier  [0,1,0,0,0,0,0,0,0,0,0,0] (there is another button for running, but only one is needed)
down          [0,0,0,0,0,1,0,0,0,0,0,0]
left          [0,0,0,0,0,0,1,0,0,0,0,0]
right         [0,0,0,0,0,0,0,1,0,0,0,0]
spin jump     [0,0,0,0,0,0,0,0,1,0,0,0]

So, the actual buttons the agent can press are represented by Xs in the gym-retro representation
[x,x,0,0,0,x,x,x,x,0,0,0]
"""


# Class used for parallel evaluation of genomes
class CustomParallelEvaluator(ParallelEvaluator):
    """
    CUSTOMIZED FROM NEAT SOURCE CODE TO PRINT PROGESS
    Runs evaluation functions in parallel subprocesses
    in order to evaluate multiple genomes at once.
    """

    def __init__(self, num_workers, eval_function, timeout=None):
        super().__init__(num_workers, eval_function, timeout=None)

        # CUSTOMIZATION: keep track of generations for recording to bk2 files
        self.generation_count = 0

    def evaluate(self, genomes, config):
        jobs = []
        genome_count = 1
        for ignored_genome_id, genome in genomes:
            # CUSTOMIZATION: also pass env=NONE, generation and genome counts so eval_genome can record bk2 files to correct folder
            jobs.append(
                self.pool.apply_async(self.eval_function, (genome, config, None, self.generation_count, genome_count))
            )
            genome_count += 1

        # assign the fitness back to each genome
        # CUSTOMIZATION: print progess (same as eval_genomes)
        genome_count = 1
        print("Genomes evaluated:", end=" ")
        for job, (ignored_genome_id, genome) in zip(jobs, genomes):
            genome.fitness = job.get(timeout=self.timeout)
            print("{}({})".format(ignored_genome_id, genome_count), end=" ", flush=True)
            genome_count += 1
        print()
        self.generation_count += 1


# The nn outputs float values and the emulator acceps only 0s or 1s
# This func asnwer the question: how loose are we in interpreting the nns outputs?
def round_input(n):
    if n >= 0.6:
        return 1
    return 0


# the NN outputs 6 bits, each representing one action in the order jump, run, down, left, right, spin jump
# this function converts the NN output to a gym retro input (array of 12 bits (or buttons))
def get_retro_action(nn_output):
    action = [0] * 12
    action[0] = round_input(nn_output[0])
    action[1] = round_input(nn_output[1])
    action[5] = round_input(nn_output[2])
    action[6] = round_input(nn_output[3])
    action[7] = round_input(nn_output[4])
    action[8] = round_input(nn_output[5])
    return action


# get the name of the button from the NN output TODO maybe use adict??
def get_button_press(action):
    buttons = set()
    if action[0]:
        buttons.add("b")    # jump
    if action[1]:
        buttons.add("y")    # run
    if action[5]:
        buttons.add("down")
    if action[6]:
        buttons.add("left")
    if action[7]:
        buttons.add("right")
    if action[8]:
        buttons.add("a")     # spin jump
    return buttons


def report_progess(env, nn_output, action, genome, current, info, ref, report, render_game, viewer, obs, speed):
    if report:
        # report stat changes
        if current["score"] != info["score"]:
            increase_score = info["score"] - current["score"]
            fit = increase_score * ref["score_rew"]
            print("scored {} points, increasing fitness by {}".format(increase_score, fit))

        if info["coins"] > current["coins"]:
            coins_collected = info["coins"] - current["coins"]
            fit = coins_collected * ref["coins_rew"]
            print("collected {} coin(s), increasing fitness by {}".format(coins_collected, fit))

        if info["yoshi_coins"] > current["yoshi_coins"]:
            yoshi_coins_collected = info["yoshi_coins"] - current["yoshi_coins"]
            fit = yoshi_coins_collected * ref["yoshi_coins_rew"]
            print("collected {} Yoshi coin(s), increasing fitness by {}".format(yoshi_coins_collected, fit))

        if info["lives"] > current["lives"]:
            print("earned a life, increasing fitness by {}".format(ref["lives_rew"]))

        if info["checkpoint"] and not current["checkpoint"]:
            print("checkpoint reached, increasing fitness by {}".format(ref["checkpoint_rew"]))

        if info["level_finish"] or info["x_pos"] > 4850:
            print("end of level reached, increasing fitness by {}".format(ref["finish_rew"]))

        if info["death"] == 9:
            print("Mario died, reducing fitness by {}".format(ref["death_pen"]))

        if current["idle"] >= ref["idle_max"]:
            print("Idle for too long, reducing fitness by {}".format(ref["idle_pen"]))

        # report general stats every x frames
        if report and (current["frame_count"] % 32 == 0 or current["done"]):
            print(
                "id: {}    fitness: {:.2f}    score: {}    x_pos: {}    frame: {}".format(
                    genome.key, current["fitness"], info["score"], info["x_pos"], current["frame_count"]
                )
            )

    # # see what the agent actually sees
    # buttons = get_button_press(action)
    # jump = buttons.intersection(set(["b"])) != set()
    # run = buttons.intersection(set(["y"])) != set()
    # if run and not jump:
    #     speed = 4
    # else:
    #     speed = 8

    # render the screen
    if render_game and (current["frame_count"] % speed == 0 or current["done"]):
        viewer.imshow(obs)

        # print("nn_outs: ", end=" ")
        # [print("{:.1f}".format(o), end=" ") for o in nn_output]
        # print()"""
        # """ print("actions: ", end=" ")
        # [print(a, end=" ") for a in action]
        # print()
        # print("buttons: ", get_button_press(action))


        # # print what mario sees in the console window
        # radius = 6
        # _ = os.system("clear")
        # print(
        #     "id: {}    fitness: {:.2f}    score: {}    x_pos: {}    frame: {}".format(
        #         genome.key, current["fitness"], info["score"], info["x_pos"], current["frame_count"]
        #     )
        # )
        # ram = getRam(env)
        # state, x, y = getInputs(ram)
        # state_mtx = np.reshape(state, (2 * radius + 1, 2 * radius + 1))
        # _ = os.system("clear")
        # # print(state_mtx)
        # #print()
        # state_n = np.reshape(getState(ram, radius)[0].split(","), (2 * radius + 1, 2 * radius + 1))
        # mm = {"0": "  ", "1": "$$", "2": "&&", "-1": "@@"}
        # for i, l in enumerate(state_n):
        #     line = list(map(lambda x: mm[x], l))
        #     if i == radius + 1:
        #         line[radius] = "X"
        #     print(line)


        # # wait for player to be ready for watching the game
        # if playback and current["frame_count"] == 0:
        #     # input("press enter to begin")
        #     for i in range(5, 0, -1):
        #         print("Starting in {}...".format(i))
        #         sleep(1)
        #     print("Starting!")

        if current["done"]:
            viewer.imshow(obs)
            sleep(speed ** 0.05 - 1)  # show last frame for a little longer


# Evaluates one genome and return its fitness by emulating gameplay with gym-retro
# Core parameters are genome, config and env
# All the others are options for recording and playback
def eval_genome(
    genome,                     # genome to evaluate
    config,                     # neat' config
    env=None,                   # emulator envirnoment
    generation_count=None,      # set up recording path
    genome_count=None,          # set up recording path
    render_game=False,          # renders the game screen
    report=False,               # report statistics of the agent's gameplay
    viewer=None,                # viewer for rendering the game (if none given, create one)
    speed=2,                    # playback speed
):
    # control variables that are updated every frame
    current = {
        "frame_count": 0,       # how many frames have passed
        "fitness": 0.0,         # agent's fitness
        "done": False,          # condition to stop the emulation
        "score": 0,             # mario's in-game score
        "farthest_x": 16,       # how far has mario travelled
        "idle": 0,              # how many frame mario hasn't progressed
        "coins": 0,             # coins collected
        "yoshi_coins": 0,       # yoshi coins collected
        "lives": 4,             # mario strts with 5 lives (4 in memory)
        "checkpoint": False,    # has mario reached the halfway checkpoint?
    }

    # reference values (reward and penalty modifiers, max or min values,...). Do not change during evaluation
    ref = {
        "x_pos_rew": 10,        # reward per distance travelled towards goal
        "finish_rew": 50000,    # reward for beating the level (automatically promotes genome to winner)
        "x_pos_pen": -2,        # penalty per frame for not making forward progress
        "idle_max": 100,        # max number of frames mario is allowed to not make forward progress 
        "idle_pen": -300,       # penalty (once) for exceding idle_max
        "death_pen": -500,      # penalty (ond) for dying
        
        # logic implemented but values not currently set (0 disables the modifiers)
        "score_rew": 0,         # reward per score increase
        "coins_rew": 0,         # reward per coin collected
        "yoshi_coins_rew": 0,   # reward per yoshi coin collected
        "lives_rew": 0,         # reward per live increase
        "checkpoint_rew": 0,    # reward per checkpoint reached
        "slow_pen": 0,          # penalty per frame (pnalize mario for taking too long to beat the game)
    }
    

    # calculates fitness based on control variables and their counterparts inside the emulator's RAM (info variable)
    def update_and_report():

        current["fitness"] += ref["slow_pen"]
        current["fitness"] += (info["score"] - current["score"]) * ref["score_rew"]
        current["fitness"] += (info["coins"] - current["coins"]) * ref["coins_rew"]
        current["fitness"] += (info["yoshi_coins"] - current["yoshi_coins"]) * ref["yoshi_coins_rew"]

        # reward mario for advancing in the level and penalize him for not advancing
        if info["x_pos"] > current["farthest_x"]:
            current["fitness"] += (info["x_pos"] - current["farthest_x"]) * ref["x_pos_rew"]
            current["farthest_x"] = info["x_pos"]
            current["idle"] = 0
        else:
            current["idle"] += 1
            current["fitness"] += ref["x_pos_pen"]

        # if mario doesnt advance for too long, end his run and penalize him a lot
        if current["idle"] >= ref["idle_max"]:
            current["fitness"] += ref["idle_pen"]
            current["done"] = True

        # reward mario for earning a life
        if info["lives"] > current["lives"]:
            current["fitness"] += ref["lives_rew"]

        # reward mario for passing through the checkpoint
        if info["checkpoint"] and not current["checkpoint"]:
            current["fitness"] += ref["checkpoint_rew"]

        # if mario finish level, boost his fitness
        if info["level_finish"] or current["farthest_x"] > 4850:
            current["fitness"] += ref["finish_rew"]
            current["done"] = True

        # if mario dies, penalize and end the run
        if info["death"] == 9:  # 9 signals the game to trigger death animation
            current["done"] = True
            current["fitness"] += ref["death_pen"]

        # report stats and render screen
        report_progess(env, nn_output, action, genome, current, info, ref, report, render_game, viewer, obs, speed)

        # update the rest of the variables (report_progress relies on some stats not being synced yet)
        current["frame_count"] += 1
        current["score"] = info["score"]
        if info["checkpoint"] and not current["checkpoint"]:
            current["checkpoint"] = True
        current["lives"] = info["lives"]
        current["coins"] = info["coins"]
        current["yoshi_coins"] = info["yoshi_coins"]


    # set up emulator. (optionally record to speficied folders (gen and genome counts))
    if not env:
        # # Setup recording dir
        # change this to record evaluation to bk2 file
        # recording_dir = pathlib.Path(PROJ_DIR).joinpath(
        #     "results", "recordings", str(generation_count), str(genome_count)
        # )
        # pathlib.Path(recording_dir).mkdir(parents=True, exist_ok=True)

        # set up game environment
        env = retro.make(
            game="SuperMarioWorld-Snes",
            info=os.path.join(PROJ_DIR, "custom_data.json"), 
            state="YoshiIsland2",
            players=1,
            # record=os.path.join(PROJ_DIR, recording_dir),         # change this to record to a bk2 file
        )
    obs = env.reset()  # set env to starting state

    # create a neural network for the given genome
    net = neat.nn.RecurrentNetwork.create(genome, config)

    # emualtion and evaluation loop
    while not current["done"]:
        # feed the network the current state of the game and get its output
        ram = getRam(env)
        state, x, y = getInputs(ram)
        nn_output = net.activate(state)
        action = get_retro_action(nn_output)

        # # debug
        # radius = 6
        # state_mtx = np.reshape(state, (2 * radius + 1, 2 * radius + 1))
        # print("state: ")
        # print(state_mtx)
        # [print("{}".format(s),end=' ') for s in state]
        # print()

        # emulate the nn's moves
        buttons = get_button_press(action)
        jump = buttons.intersection(set(["b"])) != set()
        run = buttons.intersection(set(["y"])) != set()

        # running or running while spin jumping take 4 frames for the screen to change
        if run and not jump:
            for _ in range(4):
                if current["done"]:
                    break
                obs, _, _, info = env.step(action)
                update_and_report()
        # everything else takes 8 frames
        else:
            for _ in range(8):
                if current["done"]:
                    break
                obs, _, _, info = env.step(action)
                update_and_report()
    return current["fitness"]


# Handles the evaluation of all genomes in a population
# Not used when using multi cores. CustomParallelEvaluator's evaluate function is used instead
def eval_genomes(genomes, config):
    # kep track of genreations across function calls
    if not hasattr(eval_genomes, "gen_count"):
        eval_genomes.gen_count = 0

    # setup recording
    # recording_dir = pathlib.Path(PROJ_DIR).joinpath("results", "recordings", str(eval_genomes.gen_count))
    # pathlib.Path(recording_dir).mkdir(parents=True, exist_ok=True)

    # Initialize a game at YoshiIsland2. optionally record it to the corresponding generation folder
    env = retro.make(
        game="SuperMarioWorld-Snes",
        info=os.path.join(PROJ_DIR, "custom_data.json"),
        state="YoshiIsland2",
        players=1,
        # record=os.path.join(PROJ_DIR, recording_dir),
    )

    # For every individual in the population, evaluate it's fitness and print progrss
    print("Genomes evaluated:", end=" ")
    genome_count = 1
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config, env)
        print("{}({})".format(genome_id, genome_count), end=" ", flush=True)
        genome_count += 1
    print()
    eval_genomes.gen_count += 1


def train(parallel=False):
    print("Training starting", flush=True)

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        os.path.join(PROJ_DIR, "neat-config"),
    )

    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint(pathlib.Path(PROJ_DIR).joinpath("results","checkpoints", "neat-checkpoint-24"))
    # eval_genomes.gen_count = 24

    # Adding reporters for saving stats, printing progress and saving checkpoints
    # files are saved to current working directory TODO save files inside project dir
    stats = neat.StatisticsReporter()
    checkpoint_filename = pathlib.Path(PROJ_DIR).joinpath("results", "checkpoints", "neat-checkpoint-")
    p.add_reporter(CustomStdOutReporter(True))  # see custom_reporting.py for the customization
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(2, filename_prefix=checkpoint_filename))

    # run neat and stop when mario reches the end of the level
    if parallel:
        # multiprocess setup. Use all but two available cpus
        pe = CustomParallelEvaluator(cpu_count() - 2, eval_genome)
        winner = p.run(pe.evaluate)
    else:
        winner = p.run(eval_genomes)

    # create stats files (csv)
    stats.save()

    # save the winner gnome to a file
    winner_file = pathlib.Path(PROJ_DIR).joinpath("winner.pkl")
    with open(winner_file, "wb") as output:
        pickle.dump(winner, output, 1)


def parse_args(args=[]):
    if len(args) == 0:
        print("Training with no parallelization")
        train()
        return
    if len(args) > 0 and args[0] == "parallel":
        train(parallel = True)
        return


if __name__ == "__main__":
    parse_args(sys.argv[1:])