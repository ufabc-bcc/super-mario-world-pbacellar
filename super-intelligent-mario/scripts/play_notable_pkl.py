from pathlib import Path
import sys
import re
from gym.envs.classic_control import rendering
from numpy import zeros
from time import sleep

"""
Plays all of the best or all of the worst genomes of a training session
When training, if best and worst genomes per generation are saved, this script can play them back
genomes must be saved in the formate "best-xx.pkl" where xx is number. Script uses xx for sorting plaback order

MUST BE RUN WITH PYTHON's -m OPTION

HOW TO USE:
python3 -m play_notable_pkl [option] [speed]

OPTIONS:
    best:   plays best genomes
    worst:  plays worst genomes
    speed:  plays at this speed

python3 -m super-intelligent-mario.scripts.play_notable_pkl best
python3 -m super-intelligent-mario.scripts.play_notable_pkl worst

"""

PROJ_DIR = Path(__file__).resolve().parent.parent
NOTABLE_DIR = PROJ_DIR.joinpath("results", "notable_genomes")
sys.path.append(str(PROJ_DIR))
from core.play import play


# getting best and worst
files = list(x for x in NOTABLE_DIR.iterdir() if x.is_file())

best = []
worst = []
for file in files:
    best_file = re.search(".*best.*", str(file))
    worst_file = re.search(".*worst.*", str(file))
    if best_file:
        best.append(best_file.group())

    if worst_file:
        worst.append(worst_file.group())


def key(file):
    return int(re.search("\d+", file).group())


best.sort(key=key)
worst.sort(key=key)
if len(sys.argv) <= 1:
    print("INPUT ERROR:")
    print("specify what to play, 'best' or 'worst'")
    exit(1)

speed = 4
if len(sys.argv) > 2:
    assert sys.argv[2].isdigit(), "ERROR, speed must be a number"
    speed = int(sys.argv[2])

if sys.argv[1] not in ["best", "worst"]:
    print("UNKNOWN OPTION:")
    print("specify what to play, 'best' or 'worst'")
    exit(1)

viewer = rendering.SimpleImageViewer()
transition = zeros((224, 256, 3))
viewer.imshow(transition)
for i in range(3, 0, -1):
    print("Starting in {}...".format(i))
    sleep(1)
print("Starting!")

if sys.argv[1] == "best":
    for b in best:
        play(b, timeout=False, viewer=viewer, speed=speed)
if sys.argv[1] == "worst":
    for w in worst:
        play(w, timeout=False, viewer=viewer, speed=speed)
