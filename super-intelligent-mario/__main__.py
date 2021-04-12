#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os

print(os.getcwd())


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    proc = subprocess.Popen(["python3", "-u", "../sample-reference-agents/marioRule.py"], cwd=dir_path)

    while proc:
        try:
            sig = input("type q to quit\n")
            if sig == "q":
                proc.kill()
                quit()
        except KeyboardInterrupt:
            proc.kill()
            quit()


if __name__ == "__main__":
    main()