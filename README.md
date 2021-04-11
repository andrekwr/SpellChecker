# Python Simple Spell Checker
## Natural Language Processing - INSPER 2021.1

### André Weber
### Matheus Pellizzon


<br>

### Comandos:
Para limpar o texto:
```
python cleaner.py
```
Para gerar o vocabulário a partir do texto limpo:
```
python vocab_generator.py
```
Para fazer a correção a partir do vocabulário:
```
python corrector.py "frase para correção"
```

# Melhorias feitas no projeto:

Fizemos um mlehor pré-processamento dos textos da wikipedia, removendo tags html e seus comentários, 
tags *math*, entre outras conteúdos que não pareciam relevantes para a correção de palavras. Mesmo assim, ainda há casos estranhos que podem
ser se refletem no vocabulário, como "fff".

Para a geração do vobabulário, removemos stopwords (tanto em português quanto em inglês - existiam casos de I, ), elas não agregam para a correção de outras palavras, pois suas aparições nos documentos são muito frequentes, e o vocabulário é composto pelas palavras mais 
frequentes. 

Para a correção de uma string, nos baseamos no corretor de texto do Norvig (https://norvig.com/spell-correct.html). Fizemos um smoothing
para o caso de a palavra não estar no vocabulário, evitando acesso à chaves inexistentes no dicionário. Ainda, implementamos uma correção,
ainda que mínima, de pontuação da frase. 