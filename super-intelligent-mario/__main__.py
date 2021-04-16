#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
from play import *
from train import *

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h', ["",])
    except getopt.GetoptError:
        print("ERROR: Missing argument")
        print('Corrct usage is: python3 super-intelligent-mario <opMode>')
        print("opMode can be 'train' or 'play'")
        exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('python3 super-intelligent-mario <opMode>')
            print("opMode can be 'train' or 'play'")
            exit(0)

    if(args[0] == "train"):
        train()
    elif(args[0] == "play"):
        play()
    else:
        print("wrong options")
        print('Corrct usage is: python3 super-intelligent-mario <opMode>')
        print("opMode can be 'train' or 'play'")
    return


if __name__ == "__main__":
    main(sys.argv[1:])