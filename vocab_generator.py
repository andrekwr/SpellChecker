import json
import nltk
from nltk import word_tokenize
import re
from collections import Counter


def pickLowercaseWords(tokens):
    return [token.lower() for token in tokens if re.fullmatch('\w+', token)]

def removeStopwords(word_list):
    stopwords = nltk.corpus.stopwords.words('portuguese')
    stopwords += nltk.corpus.stopwords.words('english')
    return [i for i in word_list if i not in stopwords]



#===

if __name__ == "__main__":
    data = []
    with open('dump_small_clean.jsonln', 'r', encoding="utf8") as file:
        for line in file:
            data.append(json.loads(line))

    all_words = []
    for item in data:
        texto = item['body']
        tokens = word_tokenize(texto)
        tokens = pickLowercaseWords(tokens)
        all_words += tokens

    word_counts = Counter(removeStopwords(all_words))
    word_counts_list = list(word_counts.items())
    word_counts_list_sorted = sorted(word_counts_list, key=lambda x: (-x[1], x[0]))
    vocab = word_counts_list_sorted[:10000] #10000 mais frequentes
    vocab = dict(vocab) #Vocabulario de palavras

    with open('vocab.json', 'w') as file:
        json.dump(vocab,file,indent=4)

 


