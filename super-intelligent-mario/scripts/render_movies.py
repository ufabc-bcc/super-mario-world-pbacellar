#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import retro
import time
import numpy as np
from os import walk
from os import listdir
from os.path import isfile, join, isdir
from gym.envs.classic_control import rendering


"""
Author: Pedro Braga dos Santos Bacellar
Script para visualizar uma rodada jogada pelo agente ou varias rodadas passadas em uma mesma janela de visualização

Primeiro, é preciso salvar as jogadas do agente em uma pasta.

Para isso, basta adicionar `record='nome_da_pasta'` no comando retro.make:
`env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1', players=1, record='nome_da_pasta')`

A sintaxe é
render.py [OPTIONS]
    -h                   help
    -i                   specify input file or folder
    -v, --vel=           specify speed
    -g, --last-gens=     specify number of latest generationss to render. 
                            Only works if given dir contains subfolders named numerically (0,1,3..) containing the bk2 files

Se o input for um aqruivo, renderiza o arquivo
Se o input for uma pasta que contem arquivos bk2, renderiza os arquivos,

se o input for uma pasta que contem apenas pastas nomeadas numericamente (0, 1, 2, 3, ...) 
e dentro delas houverem arquivbos bk2, renderiza na ordem das pastas (0,1,2,3,...)
Nesse caso ainda eh possivel especificara quais geracoes se quer assistir com -g ou --last-gens=

Example: ./render.py -i file.bk2 -v 5
Example: ./render.py -i dir/ --vel=5
Example: ./render.py -i dir_parent/ -last-gens=2


Pode-se ajustar a velocidade de reprodução alterando a variavel `velocidade` dentro do arquivo
`velocidade = 1`: Velocidade normal
`velocidade = 2`: Velocidade 2x
`velocidade = 3`: Velocidade 3x
...

Script inspirado em 
https://medium.com/@tristansokol/day-6-of-the-openai-retro-contest-playback-tooling-3844ba655919
https://github.com/openai/gym/issues/550
"""


viewer = rendering.SimpleImageViewer()
played_frames = 0
velocidade = 15


def render(file, velocidade=velocidade):
    try:
        movie = retro.Movie(file)
    except Exception as e:
        print(e)
        print(file)
        exit()

    movie.step()
    env = retro.make(game=movie.get_game(), state=retro.State.NONE, use_restricted_actions=retro.Actions.ALL)
    env.initial_state = movie.get_state()
    env.reset()

    frame = 1
    while movie.step():
        if frame == velocidade:
            rgb = env.render("rgb_array")
            viewer.imshow(rgb)
            frame = 1
        else:
            frame += 1

        keys = []
        for i in range(env.num_buttons):
            keys.append(movie.get_key(i, 0))
        _obs, _rew, _done, _info = env.step(keys)

        # renderiza os primeiros frames e para, esperando o usuario estar pronto para dar play no processo
        global played_frames
        played_frames += 1
        if played_frames == 3:
            rgb = env.render("rgb_array")
            viewer.imshow(rgb)
            # input("press enter to start")
            for i in range(6, 0, -1):
                print("Starting in {}...".format(i))
                time.sleep(1)
            print("Starting!")


def subfolders(path_to_parent):
    try:
        return next(walk(path_to_parent))[1]
    except StopIteration:
        return []


def render_file(file, velocidade=velocidade, last_gens=None):
    print("playing", file)
    render(file, velocidade)


def render_files(path, velocidade=velocidade, last_gens=None):
    #print(path)
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles.sort()
    for file in onlyfiles:
        if ".bk2" in file:
            transition = np.zeros((224, 256, 3))
            viewer.imshow(transition)
            render_file(join(path, file), velocidade)


def render_folders(path, velocidade=velocidade, last_gens=-1):
    folders = subfolders(path)
    folders.sort(key=int)
    if last_gens > -1:
        folders = folders[len(folders) - int(last_gens) :]
        print("Rendering only last", last_gens, "generation(s)", folders)
    else:
        folders = folders[len(folders) - 2 :]
        print("rendering only last 2 generations,", folders)
    for folder in folders:
        render_files(join(path, folder), velocidade)


def render_folders_from_multiprocs(path, velocidade=velocidade, last_gens=-1):
    folders = subfolders(path)
    folders.sort(key=int)

    if last_gens > -1:
        folders = folders[len(folders) - int(last_gens) :]
        print("Rendering only last", last_gens, "generation(s)", folders)
    else:
        folders = folders[len(folders) - 2 :]
        print("rendering only last 2 generations,", folders)

    for subs in folders:

        folders = subfolders(path+str(subs))
        folders.sort(key=int)

        folders = [join(path, subs, folder) for folder in folders]

        for f in folders:
            print(f)
            render_files(f, velocidade)


def usage():
    print("Usage: [OPTION]...")
    print("Example: ./render.py -i file.bk2 -v 5")
    print("Example: ./render.py -i dir/ --vel=5")
    print("Example: ./render.py -i dir_parent/ -last-gens=2")
    print("render.py [OPTIONS]")
    print("    -h                   help")
    print("    -i                   specify input file or folder")
    print("    -v, --vel=           specify speed")
    print("    -g, --last-gens=     specify number of latest gens to render. Only works if given dir contains subfolders named numerically (0,1,3..) containing the bk2 files ")

def run():
    global velocidade
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:v:g:m", ["help", "input=", "vel=", "last-gens=", "mult-dirs"])
        if not opts:
            raise getopt.GetoptError("Missing arguments")

        if "-i" not in [opt for opt, arg in opts] and "--input" not in [opt for opt, arg in opts]:
            raise getopt.GetoptError("Must provide input file or folder")

    except getopt.GetoptError as err:
        print(err)
        usage()
        exit(2)


    user_input = None
    last_gens = -1
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            exit(0)
        elif opt in ("-i", "--input"):
            user_input = arg
            if isdir(arg):
                if subfolders(arg):
                    if subfolders(arg+"0"):
                        func= render_folders_from_multiprocs
                    else:
                        func = render_folders
                else:
                    func = render_files
            else:
                func = render_file
        elif opt in ("-v", "--vel"):
            velocidade = int(arg)
        elif opt in ("-g", "--last-gens"):
            last_gens = int(arg)
        else:
            print("option unhandled", opt)
            exit(2)

    if "-g" in [opt for opt, args in opts] or "--last-gens" in [opt for opt, args in opts]:
        assert subfolders(user_input), "When running latest gens, input dir must contain subdirs with the bk2 files"

    func(user_input, velocidade, last_gens)

if __name__ == "__main__":
    run()