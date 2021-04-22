#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import getopt
from core import train_screen, train_memory, play


"""
To run this project use:
    ``` python3 [train|play] [options] ```

options for op_mode `train`:
    `parallel`  :   if `parallel` is given, uses multi core to speed up processing (uses all but 2 available cores). Default is single core

options for op_mode `play`:
    `file`      :   if none give, plays default `winner.pkl` in project root
    `speed`     :   default is 2 (defined in play.py) 

"""


def usage():
    print("Correct usage is: python3 super-intelligent-mario <op_mode> <file>")
    print("op_mode can be 'train', 'train parallel' or 'play'")
    print("if op_mode = play, a file may be selected. Otherwise, winner.pkl is played")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", [""])
    except getopt.GetoptError:
        print("ERROR: Missing argument")
        usage()
        exit(2)

    for opt, arg in opts:
        if opt == "-h":
            usage()
            exit(0)

    # train aceppts argument `parallel` to use multicores during training. Default is single core
    if args[0] == "train":
        if len(args) > 1:
            train_memory.parse_args(args[1:])
        else:
            train_memory.parse_args()
    # play accepts arguments `file` and `speed`. Default is winner.pkl in PROJ_DIR and speed = 2
    elif args[0] == "play":
        if len(args) <= 1:
            play.parse_args()
            return
        if len(args) == 2:
            play.parse_args(args[1:])
            return
        if len(args) == 3:
            play.parse_args(args[2:])
            return
    else:
        print("wrong options")
        usage()
    return


if __name__ == "__main__":
    main(sys.argv[1:])