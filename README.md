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

Fizemos um pré-processamento dos textos da wikipedia, através do arquivo ```
cleaner.py```
 para remover formatação html e seus comentários, 
tags do tipo *math*, própria formatação da wikipedia, entre outros conteúdos que não pareciam relevantes para a correção de palavras. Contudo, ainda há casos estranhos que podem ser apresentados no vocabulário, como "fff", mas que podem ser tratados posteriormente analisando a probabilidade da palavra.

Para a geração do vobabulário, através do arquivo ``` vocab_generator.py``` removemos stopwords providas pela biblioteca nltk (tanto em português quanto em inglês - existiam casos de I, the, ...), elas não agregam para a correção de outras palavras, pois suas aparições nos documentos são muito comuns, e o vocabulário é composto pelas palavras mais 
frequentes. 

Para a correção de uma string nos baseamos no corretor de texto do Diretor de Pesquisa da Google, Peter Norvig (https://norvig.com/spell-correct.html), feita através do arquivo ```corrector.py```. Fizemos um smoothing para o caso de uma palavra não estar contida no vocabulário, evitando acesso à chaves inexistentes no dicionário. Também implementamos uma correção, ainda que mínima, de pontuação da frase. 
