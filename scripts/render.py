#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Pedro Braga dos Santos Bacellar
Script para visualizar uma rodada jogada pelo agente ou varias rodadas passadas em uma mesma janela de visualização

Primeiro, é preciso salvar as jogadas do agente em uma pasta.

Para isso, basta adicionar `record='nome_da_pasta'` no comando retro.make:
`env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1', players=1, record='nome_da_pasta')`

Para visualizar as jogadas, use 
`python render.py [pasta/arquivo.bk2 ou nome_da_pasta_com_os_arquivos/]`

Exemplo para dar replay em todos os arquivos de uma pasta: 
`python render.py nome_da_pasta_com_os_arquivos/`

Note a "/" ao final do caminho, indicando que é uma pasta. No windows, a barra é "\"

Finalmente, pode-se ajustar a velocidade de reprodução alterando a variavel `multiplicador`
`multiplicador = 0`: Velocidade normal
`multiplicador = 1`: Velocidade 2x
`multiplicador = 2`: Velocidade 3x
...

Script inspirado em 
https://medium.com/@tristansokol/day-6-of-the-openai-retro-contest-playback-tooling-3844ba655919
https://github.com/openai/gym/issues/550
"""

import sys
import retro
from os import listdir
from os.path import isfile, join, isdir
from gym.envs.classic_control import rendering

played_frames=0
def render(file):
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

    frame = 0
    multiplicador = 2
    while movie.step():
        if frame == multiplicador:
            rgb = env.render('rgb_array')
            viewer.imshow(rgb)
            frame = 0
        else:
            frame += 1

        keys = []
        for i in range(env.num_buttons):
            keys.append(movie.get_key(i, 0))
        _obs, _rew, _done, _info = env.step(keys)
        
        # renderiza os primeiros frames e para, esperando o usuario estar pronto para dar play no processo
        global played_frames
        played_frames += 1
        if(played_frames == 3):
            input("press enter to start")


viewer = rendering.SimpleImageViewer()
if isdir(sys.argv[1]):
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    for file in onlyfiles:
        if ".bk2" in file:
            print('playing', file)
            render(sys.argv[1]+file)
else:
    print('playing', sys.argv[1])
    render(sys.argv[1])






















""" 
def render3(file):
    from gym.envs.classic_control import rendering

    def scale(A, B, k):     # fill A with B scaled by k
        Y = A.shape[0]
        X = A.shape[1]
        for y in range(0, k):
            for x in range(0, k):
                A[y:Y:k, x:X:k] = B
        return A


    def repeat_upsample(rgb_array, k=1, l=1, err=[]): #https://gist.github.com/mttk/74dc6eaaea83b9f06c2cc99584d45f96
        # repeat kinda crashes if k/l are zero
        if k <= 0 or l <= 0: 
            if not err: 
                print ("Number of repeats must be larger than 0, k: {}, l: {}, returning default array!").format(k, l)
                err.append('logged')
            return rgb_array

        # repeat the pixels k times along the y axis and l times along the x axis
        # if the input image is of shape (m,n,3), the output image will be of shape (k*m, l*n, 3)


        return np.repeat(np.repeat(rgb_array, k, axis=0), l, axis=1)


    viewer = rendering.SimpleImageViewer()
    movie = retro.Movie(file)
    movie.step()
    env = retro.make(game=movie.get_game(), state=retro.State.NONE, use_restricted_actions=retro.Actions.ALL)
    env.initial_state = movie.get_state()   
    env.reset()

    frame = 0
    framerate = 2
    while movie.step():
        if frame == framerate:
            rgb = env.render('rgb_array')
            k=4
            A = np.zeros((rgb.shape[0] * k, rgb.shape[1] *k, rgb.shape[2]), dtype = rgb.dtype)
            #upscaled = scale(A, rgb, k)
            upscaled=repeat_upsample(rgb,k, k)

            viewer.imshow(upscaled)
            frame = 0
        else:
            frame += 1

        keys = []
        for i in range(env.num_buttons):
            keys.append(movie.get_key(i, 0))
        _obs, _rew, _done, _info = env.step(keys)



def render2(file):
    is_ipython = 'inline' in matplotlib.get_backend()
    if is_ipython: from IPython import display

    movie = retro.Movie(file)
    movie.step()
    env = retro.make(game=movie.get_game(), state=retro.State.NONE, use_restricted_actions=retro.Actions.ALL)
    env.initial_state = movie.get_state()
    env.reset()

    frame = 0
    framerate = 2
    a = env.render(mode='rgb_array')
    myImg = plt.imshow(a)
    while movie.step():
        print("here")
        if frame == framerate:
            a = env.render(mode='rgb_array')
            plt.figure()
            myImg.set_data(a)
            plt.draw()
            frame = 0
        else:
            frame += 1
        keys = []
        for i in range(env.num_buttons):
            keys.append(movie.get_key(i, 0))
        _obs, _rew, _done, _info = env.step(keys)
    env.close()
    if is_ipython: display.clear_output(wait=True)
    plt.show()



def render(file):
    movie = retro.Movie(file)
    movie.step()
    env = retro.make(game=movie.get_game(), state=retro.State.NONE, use_restricted_actions=retro.Actions.ALL)
    env.initial_state = movie.get_state()
    env.reset()
    frame = 0
    framerate = 10
    while movie.step():
        if frame == framerate:
            env.render()
            frame = 0
        else:
            frame += 1

        keys = []
        for i in range(env.num_buttons):
            keys.append(movie.get_key(i, 0))
        _obs, _rew, _done, _info = env.step(keys)
    env.close()
 """
