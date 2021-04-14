from . import CORE_DIR
import pickle
import retro
import os

#from utils.rominfo import *
#from utils.utils import *

custom_data = os.path.join(CORE_DIR,"cfg/custom_data.json")
custom_scenario= os.path.join(CORE_DIR,"cfg/custom_scenario.json")

# An action is an array of 12 bits. Each bit represents a button on the controller
# [0,0,0,0,0,0,0,0,0,0,0,0]
# But not all buttons are interesting (like start, select, R and L)
#
# These are the base actions the agent can make (the agent can also combine any number of base actions)
# up            [0,0,0,0,1,0,0,0,0,0,0,0]
# down          [0,0,0,0,0,1,0,0,0,0,0,0]
# left          [0,0,0,0,0,0,1,0,0,0,0,0]
# right         [0,0,0,0,0,0,0,1,0,0,0,0]
# run modifier  [0,1,0,0,0,0,0,0,0,0,0,0] (there is another button for running, but only one is needed)
# jump          [1,0,0,0,0,0,0,0,0,0,0,0]
# spin jump     [0,0,0,0,0,0,0,0,1,0,0,0]

# 4830 end of level

def train():
    print("training")
    
    # creating game state at the beginning of YoshiIsland2
    env = retro.make(
        game="SuperMarioWorld-Snes", scenario=custom_scenario, info=custom_data, state="YoshiIsland2", players=1, record="bk2"
    )
    env.reset()

    # Sertting up memory variables


    done = False
    totRew = 0
    while not done:
        #action = env.action_space.sample()
        action = [0,0,0,0,0,0,0,1,0,0,0,0]
        ob, rew, done, info = env.step(action)
        env.render()
        totRew+=rew
        print(action, " ", info, "  rew: ", "{:.2f}".format(rew), "   totRew: ", "{:.2f}".format(totRew))
        