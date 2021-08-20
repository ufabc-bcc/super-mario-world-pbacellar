# Super Mario World IA

## Descrição

Este projeto foi desenvolvido para a disciplina de Inteligência Artificial da UFABC, ministrada pelo professor [Fabricio Olivetti](https://github.com/folivetti)

Utilizo o algorítmo NEAT, implementado por [CodeReclaimers](https://github.com/CodeReclaimers/neat-python) para desenvolver um agente inteligente capaz de vencer a fase YoshiIsland2 do jogo Super Mario World do SNES.

[video](res/Winner.mp4)

## Dependências

Esse projeto precisa de python 3.8 (talvez funcione com 3.6 e 3.7) e usa NEAT-Python 0.92, gym-retro 0.8.0 e opencv-python 4.5.1.48.

Para instalar todas as dependências, rode, na raiz do repositório:

```pip install -r requirements.txt```

ou

```pipenv install```

ou

```pipenv install -r requirements.txt```

Você também vai precisar instalar a rom do jogo no ambiente do gym retro:

```python3 -m retro.import rom.sfc```

Alternativamente, copie `rom.sfc` para o diretório ```site-packages/retro/data/stable/SuperMarioWorld-Snes/```

* Se você usa pipenv, deve estar em

  ```~/.local/share/virtualenvs/super-mario-world-XXXXXXXXX/lib/python3.8/site-packages/retro/data/stable/SuperMarioWorld-Snes/```

## Instruções de uso

O projeto foi desenvolvido em um abiente virtual isolado usando a ferramente [pipenv](https://pipenv.pypa.io/en/latest/) e seu uso é recomendado (por causa dos scripts, veja arquivo pipfile), mas não necessário para rodar este projeto.

Todos os comandos devem ser rodados na raíz do repositório (onde está o arquivo pipfile).

### **Treinamento**

Para treinar um agente novo do zero:

* Sem usar paralelismo:

  * ```python3 -u super-intelligent-mario train```
  * ```pipenv run train```

* Com paralelismo:

  * ```python3 -u super-intelligent-mario train parallel```
  * ```pipenv run train parallel```

O treinamento em paralelo leva em média 20 minutos (para mim) e salva na pasta results:

* checkpoints de cada geração (`checkpoints/`)
* os melhores e piores genomas de cada geração (`notable_genomes/`)
* (opcional) gravações no formato `bk2` de todas as simulações de todos os individuos
  * Para habilitar isso, é preciso descomentar uma linha na chamada da função ```retro.make``` e também algumas linhas que a precedem:
    * ```# record=os.path.join(PROJ_DIR, recording_dir)```
    * ```# recording_dir = pathlib.Path(PROJ_DIR).joinpath("results", "recordings", str(generation_count), str(genome_count))```
    * ```# pathlib.Path(recording_dir).mkdir(parents=True, exist_ok=True)```

Caso interrompa um sessão de treinamento no meio, é possível recomçar o treinamento usando o mesmo comando. Para isso, na seção abaixo, no `train_memory.py` ou `train_screen.py`, altere o código abaixo, inserindo o checkpoint que deseja restaurar

```python
p = neat.Population(config)
# p = neat.Checkpointer.restore_checkpoint(pathlib.Path(PROJ_DIR).joinpath("results","checkpoints", "neat-checkpoint-24"))
# eval_genomes.gen_count = 24
```

para

```python
#p = neat.Population(config)
p = neat.Checkpointer.restore_checkpoint(pathlib.Path(PROJ_DIR).joinpath("results","checkpoints", "SEU-CHECKPOINT-DESEJADO")) # insira o checkpoint que deseja restaurar
eval_genomes.gen_count = 24
```

**O treinamento padrão** (módulo `train_memory.py`) usa como input para a rede neural uma pequena parcela de informações (chão, inimigos, obstáculos) obtidas da memória RAM do jogo através da biblioteca fornecida pelo professor `rominfo.py` e levemente alterada por mim.

**O treinamento alternativo** (módulo `train_screen.py`) se baseia na tela do jogo com resolução reduzida. Esse modo não é recomendado, pois demora muito. Para treinar dessa forma, basta alterar no arquivo `__main__.py` as instâncias de `train_memory` para `train_screen`

### **Reprodução**

Para reproduzir um genoma use:

* ```python3 -u super-intelligent-mario play [ARQUIVO.PKL] [VELOCIDADE]```
* ```pipenv run play [ARQUIVO.PKL] [VELOCIDADE]```

Além do arquivo, função `play` também aceita como parâmetro opcional a velocidade de reprodução (padrão é 2, tente usar 1 ou 10)

## Melhor genoma (até agora)

O melhor genoma treinado até agora (por mim) é o `winner.pkl` e encontra-se na pasta `best_winner_results` para fins de exemplo. Na mesma pasta, há vídeos de seu treinamento e desempenho, estatísticas de seu treinamento, checkpoints e genoams notáveis do treinamento (dica, é possível acompanhar evolução com um dos scripts abaixo)

## Scripts (fase alpha)

Na pasta `scripts/`

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
    ├── best_winner_results         # Exemplo de um vencedor
    │       └── ...
```
