# Projeto 2: Super Mario World - Inteligência Artificial - 2021.Q1


refs

https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6







Prof. Fabrício Olivetti de França (folivetti@ufabc.edu.br)

## Enunciado

Para esse projeto vocês devem implementar um agente inteligente capaz de jogar a fase *YoshiIsland2* do jogo Super Mario World utilizando um dos algoritmos apresentados em aula na segunda metade do curso, do livro texto ou de algum artigo científico.

Os algoritmos devem ser escritos em Python e farão uso da biblioteca Retro Gym (https://github.com/openai/retro).

Para carregar o jogo você deve necessariamente utilizar essa linha de código:

```
env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', players=1)
```

## Instruções de instalação:

- Instale a biblioteca Retro Gym seguindo as instruções em: https://github.com/openai/retro
- Copie a ROM do jogo para o diretório *site-packages/retro/data/stable/SuperMarioWorldSnes/* com o nome *rom.sfc* (se estiver utilizando o Anaconda, ele deve
estar em *~/anaconda3/lib/python3.6/*)
- Se tudo estiver funcionando corretamente, você conseguirá executar os scripts marioRule.py e marioAstar.py
- Estude os códigos marioRule.py, rominfo.py, utils.py e marioAstar.py para entender o funcionamento da biblioteca.

## Entregas

Esse projeto terá múltiplas datas de entrega via Github Classroom em que, para efeito de correção, será utilizado o *commit* da data correspondente a entrega:

1. 31/03/2021   - Relatório reportando resultados iniciais e dificuldades
2. 16/04/2021 - Relatório final
3. 19/04/2021 - Vídeo de apresentação

Além dos códigos, o aluno deverá gravar um vídeo apresentando sua solução. No início do vídeo o aluno deve mostrar o rosto e dizer claramente seu nome e RA.

## Avaliação

A nota será atribuída em relação a:

- P1: organização e estruturação do código ($[0, 3]$)
- P2: corretude das soluções ($[0, 4]$)
- P3: rank no progresso dentro da fase ($[0, 3]$)

O rank no tempo de execução será:

- Os $10\%$ melhores agentes: 3 pontos
- Os $10\%$ piores agentes: 1 ponto
- Entre esses dois: 2 pontos
- Caso o agente não ultrapasse o desempenho do código *marioRule.py*: 0 pontos

Não serão permitidas soluções *hard-coded*.
