# Projeto 2: Super Mario World - Inteligência Artificial - 2021.Q1

Feito por:

Pedro Braga dos Santos Bacellar

RA 11046713

github: [pbacellar](https://github.com/pbacellar)

## TL;DR:

Video [https://youtu.be/w46w_6PJ0DY](https://youtu.be/w46w_6PJ0DY)

Todos os comandos a partir da raiz do repo:

* ```pip install -r requirements.txt```

* play
  * ```python3 -u super-intelligent-mario play [ARQUIVO.PKL] [VELOCIDADE]```<br>
    (Winner eh o super-intelligent-mario/best_winner_results/winner.pkl) (velocidade padrao eh 2)

* train
  * ```python3 -u super-intelligent-mario train``` ou ```python3 -u super-intelligent-mario train parallel```<br>
    (da uma olhada na pasta results depois) (aqui leva em média 22 minutos para treinar um vencedor)

* roda os melhores ou piors
  * ```python3 -m super-intelligent-mario.scripts.play_notable_pkl [BEST|WORST] [velocidade]```<br>
    (roda isso depois de treinar ou depois de um tempo treinando)


## Descrição

Este projeto utiliza o algorítmo NEAT implementado por CodeReclaimenrs ([github](https://github.com/CodeReclaimers/neat-python)) para desenvolver um agente inteligente capaz de vencer a fazer YoshiIsland2 do jogo Super Mario World do SNES.

Video de apresentação: [https://youtu.be/w46w_6PJ0DY](https://youtu.be/w46w_6PJ0DY)

## Dependências

Este projeto usa NEAT-Python 0.92, gym-retro 0.8.0 e opencv-python 4.5.1.48.

Para instalar todas as dependências, rode, na raiz do repositório:

```pip install -r requirements.txt```

ou

```pipenv install -r requirements.txt```

## Instruções de uso

O projeto foi desenvolvido em um abiente virtual isolado usando a ferramente [pipenv](https://pipenv.pypa.io/en/latest/) e seu uso é recomendado (por causa dos scripts, veja arquivo pipfile), mas não necessário para rodar este projeto.

Todos os comandos devem ser rodados na raíz do repositório.

### Treinamento

Para treinar um agente novo do zero:

Sem usar paralelismo:

* ```python3 -u super-intelligent-mario train```
* ```pipenv run train```

Usando paralelismo para acelerar o processamento:

* ```python3 -u super-intelligent-mario train parallel```
* ```pipenv run train parallel```

O treinamento salva na pasta results:

* checkpoints de cada geração (checkpoints/)
* os melhores e piores genomas de cada geração (notable_genomes/)
* (opcional) gravações no formato bk2 de todas as simulações de todos os individuos
  * Para habilitar isso, é preciso descomentar uma linha na chamada da função ```retro.make``` e também algumas linhas que a precedem:
    * ```# record=os.path.join(PROJ_DIR, recording_dir)```
    * ```# recording_dir = pathlib.Path(PROJ_DIR).joinpath("results", "recordings", str(generation_count), str(genome_count))```
    * ```# pathlib.Path(recording_dir).mkdir(parents=True, exist_ok=True)```

O treinamento `train_memory` padrão usa como input para a rede neural uma pequena parcela de informações (chão, inigmos, obstáculos) obtidas da memória RAM do jogo através da biblioteca fornecida pelo professor `rominfo.py` e levemente alterada por mim.

Há também a opção treinar o agente com a tela do jogo com resolução reduzida (`train_screen`). Para isso, basta alterar `train_memory...` na `main` para `train_screen...`

Para retomar uma sessão de treinamento, é preciso alterar as seguintes linhas, descomentando o que está comentado e comentando o que não está, além de especificar qual o checkpoint que deve ser usado:

```python
p = neat.Population(config)
# p = neat.Checkpointer.restore_checkpoint(pathlib.Path(PROJ_DIR).joinpath("results","checkpoints", "neat-checkpoint-24"))
# eval_genomes.gen_count = 24
```

### Reprodução

Para reproduzir um genoma use:

* ```python3 -u super-intelligent-mario play [ARQUIVO.PKL] [VELOCIDADE]```
* ```pipenv run play [ARQUIVO.PKL] [VELOCIDADE]```

Além do arquivo, função `play` também aceita como parâmetro opcional a velocidade de reprodução (padrão é 2)

## Melhor genoma

O melhor genoma treinado até agora é o `winner.pkl` e encontra-se na pasta `best_winner_results`, junto com statisticas de seu treinamento, checkpoints e genoams notáveis do treinamento (dica, é possível acompanhar evolução com um dos scripts abaixo)

## Scripts

* `play_notable_pkl`

    Após rodar um treinamento, é possível reprodozuir todos os melhores ou piores genomas para acompanhar a evolução do agente. O script reproduz do primeiro genoma ao último
  * ```python3 -m super-intelligent-mario.scripts.play_notable_pkl [BEST|WORST] [velocidade]```
  * ```pipenv run play_notable [best|worst] [velocidade]```

* `render_movies`

    Caso tenha gravado toda a sessão de treino em arquivos bk2, esse script possui diversas opções para reproduçao
    Como não tem sido muito usado, para informações de uso, veja documentação dentro do próprio script.

    O exemplo abaixo reproduz todos os arquivos bks na pasta recordings em ordem (do prieiro ao último)
  * ```python3 -u super-intelligent-mario/scripts/render_movies.py -i super-intelligent-mario/results/recordings/```
  * ```pipenv run render```

    já este, reproduz apenas os vídeos das últimas 3 gerações
  * ```python3 -u super-intelligent-mario/scripts/render_movies.py -i super-intelligent-mario/results/recordings/ -g 3```
  * ```pipenv run render -g 3```

* `clean_training.sh`

    limpa uma sessão de treinamento, esvaziando as pastas `checkpoints`, `recordings` e `notable_genomes`, através de mini scripts dentro das próprias pastas (caso queira esvaziá-las individualmente)
  * ```super-intelligent-mario/scripts/clean_training.sh```
  * ```pipenv run clean```

## Estrutura do código

```shell
.
├── Pipfile                         # para uso com pipenv
├── Pipfile.lock                    # para uso com pipenv
├── README.md
├── requirements.txt
├── rom.sfc
└── super-intelligent-mario
    ├── __init__.py
    ├── __main__.py
    ├── core
    │   ├── __init__.py
    │   ├── custom_reporting.py
    │   ├── play.py
    │   ├── rominfo.py
    │   ├── train_memory.py         
    │   └── train_screen.py
    ├── scripts
    │   ├── bk2_to_mp4.py
    │   ├── clean_training.sh
    │   ├── play_notable_pkl.py
    │   └── render_movies.p
    ├── custom_data.json
    ├── neat-config
    ├── neat-config-screen
    ├── winner.pkl
    ├── results
    │       └── ...
    ├── best_winner_results
    │       └── ...
```
