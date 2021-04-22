#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import PROJ_DIR
from core import train_memory, train_screen

import neat
import retro
import os
import sys
import pickle
from gym.envs.classic_control import rendering
import numpy as np
from time import sleep


"""
Simple module that replays a genome saved in .pkl format by making use of the eval_genome function in train.py
Can be run as a module with python3 -m
"""


def play(file=None, timeout=True, viewer=None, env = None, speed=2):
    if file:
        winner_path = file
    else:
        # look for winner in PROJ_DIR
        winner_path = os.path.join(PROJ_DIR, "winner.pkl")
    try:
        winner_genome = pickle.load(open(winner_path, "rb"))
    except FileNotFoundError as e:
        print("Winner not found")
        print(e)
        exit(1)

    print("playing {}".format(winner_path))

    # read config file
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        os.path.join(PROJ_DIR, "neat-config"),
        #os.path.join(PROJ_DIR, "neat-config-screen"),
        
    )
    if not env:
        env = retro.make(
            game="SuperMarioWorld-Snes",
            info=os.path.join(PROJ_DIR, "custom_data.json"),  # in-game variables and their addresses
            state="YoshiIsland2",
            players=1,
            # record=os.path.join(PROJ_DIR, "results","recordings") # create a bk2 of the winner
        )

    
    if not viewer:
        viewer = rendering.SimpleImageViewer()
    transition = np.zeros((224, 256, 3))
    viewer.imshow(transition)
    if timeout:
        for i in range(3, 0, -1):
            print("Starting in {}...".format(i))
            sleep(1)
        print("Starting!")
    train_memory.eval_genome(winner_genome, config, env, render_game=False, report=False, speed=speed, viewer=viewer)
    #train_screen.eval_genome(winner_genome, config, env, render_game=True, report=True, speed=speed, viewer=viewer)


def parse_args(args=[]):
    if len(args) == 0:
        print("Playing defautl winner.pkl, with default speed")
        play()
        return

    if len(args) == 1:
        if args[0].isdigit():
            speed = int(args[0])  # treat first arg as speed and play deafult winner
            print("Playing defautl winner.pkl, with speed {}".format(speed))
            play(speed=speed)
        else:
            winner = args[0]  # treat first arg as winner
            print("Playing {}, with default speed".format(winner))
            play(file=winner)
        return

    if len(args) == 2:
        winner = args[0]  # treat first arg as winner
        assert args[1].isdigit(), "Speed must be a number"
        speed = int(args[1])  # treat second arg as speed
        print("Playing {}, with speed {}".format(winner, speed))
        play(file=winner, speed=speed)
        return


if __name__ == "__main__":
    parse_args(sys.argv[1:])