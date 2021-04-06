import json
import nltk
from nltk import word_tokenize
import re 
from nltk.tokenize import RegexpTokenizer
import argparse

LOWERCASE = [chr(x) for x in range(ord('a'), ord('z') + 1)]
LOWERCASE_OTHERS = [chr(x) for x in range(129, 164)] # ü até ú https://theasciicode.com.ar/
LETTERS = LOWERCASE + LOWERCASE_OTHERS

with open('vocab.json', 'r') as file:
    vocab = json.loads(file.read())

def edit1(text):
    words = []
    
    # Fase 1: as remoçoes.
    for p in range(len(text)):
        new_word = text[:p] + text[p + 1:]
        if len(new_word) > 0:
            words.append(new_word)
        
    # Fase 2: as adições.
    for p in range(len(text) + 1):
        for c in LETTERS:
            new_word = text[:p] + c + text[p:]
            words.append(new_word)
    
    # Fase 3: as substituições.
    for p in range(len(text)):
        orig_c = text[p]
        for c in LETTERS:
            if orig_c != c:
                new_word = text[:p] + c + text[p + 1:]
                words.append(new_word)
    
    return set(words)

def edit2(text):
    words1 = edit1(text)
    words2 = set()
    for w in words1:
        candidate_words2 = edit1(w)
        candidate_words2 -= words1
        words2.update(candidate_words2)
    words2 -= set([text])
    return words2


def candidates(word):
    editD1 = [w for w in edit1(word) if w in vocab]
    editD2 = [w for w in edit2(word) if w in vocab]
    if word in vocab:
        return [word]
    elif editD1:
        return editD1
    elif editD2:
        return editD2
    else:
        return [word]
 
V = 1e5
def P(word, N=sum(vocab.values())):
    count = vocab[word] if word in vocab else 0
    return (count+1) / (N+V) # Perguntar tecnica de smoothing.


 
def correction(word):
    return max(candidates(word), key=P)


 
def tokenCorrection(text):
    tokenizer = RegexpTokenizer("(?:[\w']+)|(?:[,.;!?:])")
    tokens = tokenizer.tokenize(text)
    corrected_tokens = []
    for t in tokens:
        if t in ",.;!?:":
            corrected_tokens += [t]
        elif t.isdigit():
            corrected_tokens += [t]
        else:
            if t in nltk.corpus.stopwords.words('portuguese'):
                corrected_tokens += [t]
            else:
                corrected_tokens += [correction(t)]

    return " ".join(corrected_tokens)

 
def punctuationCorrection(text):
    text = re.sub(r"\s([,.;!?:](?:\s|$))", r"\1", text)
    return re.sub(r"(^|[.?!])\s*(\w)", lambda p: p.group(0).upper(), text)


 
def textCorrection(text):
    funcs = [
        tokenCorrection,
        punctuationCorrection
    ]
    
    x = text
    for func in funcs:
        x = func(x)
    
    return x

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prefix_chars='@')

    parser.add_argument("phrase",help="Phrase to correct",type=str)
    args = parser.parse_args()

    #Tests strings
    strings = [
    "o matheus é efiiente",
    "o trabalo está bom",
    "bom di, pesoal",
    "irei ao mercaso. quer de algo?",
    "o andré é muito bacana"
    ]

    print(textCorrection(args.phrase))
    

 
