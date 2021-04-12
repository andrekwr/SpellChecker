import json
import re

#Remove URLs
## Functions to clean wikipedia's text.
def removeUrl(texto):
    # https://www.geeksforgeeks.org/python-check-url-string/
    pattern = r"""
        (?i)
        \b  
        (?:
            https?://
        |
            www
            \d{0,3}
            [.]
        |
            [a-z0-9.-]+
            [.]
            [a-z]{2,4}
            /
        )
        (?:
            [^\s()<>]+
        |
            (
            (?:
                [^\s()<>]+
            |
                (
                [^\s()<>]+
                )
            )*
            )
        )+
        (?:
            (
            (?:
                [^\s()<>]+
            |
                (
                [^\s()<>]+
                )
            )*
            )
        |
            [^\s`!()[]{};:'".,<>?«»“”‘’]
        )
    """
    repl = ""
    matcher = re.compile(pattern, re.VERBOSE)
    return matcher.sub(repl, texto)

#Remove Wikipedia hyperlinks
def removeWikipediaLinks(text):
    pattern = r"\[\[(?:[^|]*?\|)*?([^|]*?)\]\]"
    repl = r"\1"
    matcher = re.compile(pattern)
    return matcher.sub(repl, text)

#Remove html tag ref
def removeRef(text):
    return re.sub(r"<ref(?:.*)?>.*?(?:</ref>)?", "", text)

#Remove math tag 
def removeMath(text):
    return re.sub(r"<math(?:.*)?>.*?(?:</math>)?", "", text)

#Remove tags delimited by <> characters
def removeOtherTags(text):
    return re.sub(r"<.*?>(.*?)<.*?>", r"\1", text)

#Remove wikipedia formatting
def removeHtmlFormat(text):
    return re.sub(r'\w+=".*"', "", text)

#Remove wikipedia formatting
def removeOtherWikiFormat(text):
    return re.sub(r"\w+=.+", " ", text)

#Remove quotation mark
def removeQuotationMark(text):
    pattern = r"""(['"]+)(.*?)\1"""
    matcher = re.compile(pattern)
    return matcher.sub(r"\2", text)

#Remove equal symbol
def removeEqual(text):
    return text.replace("=", " ")

#Remove braces
def removeBraces(text):
    pattern = r"{.*?}"
    matcher = re.compile(pattern)
    return matcher.sub("", text)

#Remove brackets
def removeBrackets(text):
    pattern = r"\[.*?\]"
    matcher = re.compile(pattern)
    text = matcher.sub("", text)
    text = text.replace("]", "")
    return text.replace("[", "")

#Remove formatting <!--
def removeHtmlComment(texto):
    pattern = r"<!--.*?-->"
    matcher = re.compile(pattern)
    return matcher.sub("", texto)

#Remove asterisk
def removeAsterisk(texto):
    texto = texto.replace("*", "")
    return texto

#Remove pixel indicative
def removePx(text):
    return re.sub(r"(?:\d+x)?\d+px", " ", text)

#Remove dash
def removeDash(text):
    return re.sub(r"\s+[-–]\s+", " ", text)

#Remove parentheses
def removeParentheses(text):
    text = text.replace("(", "")
    return text.replace(")", "")

#Remove ordinal indicator
def removeUpperO(text):  # °
    return text.replace("\u00ba", "")

#Remove digits
def removeDigits(text):
    return re.sub("\d+", "", text)

#Remove irrevelent characters
def removeOtherSymbols(text):
    toRemove = ["|", ",", "\n", "\t", ";"]
    x = text
    for i in toRemove:
        x.replace(i, "")
    return x

#Remove wikipedia templates: double braces
def removeWikipediaTemplates(text):
    count = 0
    spans_proibidos = []
    for item in re.finditer(r"{{|}}", text):
        if item[0] == "{{":
            if count == 0:
                inicio = item.span()[0]
            count += 1
        else:
            count -= 1
            if count == 0:
                fim = item.span()[1]
                spans_proibidos.append((inicio, fim))

    clean_text = ""
    inicio = 0
    for span in spans_proibidos:
        fim, novo_inicio = span
        clean_text += text[inicio:fim]
        inicio = novo_inicio

    clean_text += text[inicio:]
    return clean_text

#Remove braces
def removeRemainingBraces(text):
    text = text.replace("{", "")
    return text.replace("}", "")


def clearText(text):
    funcs = [
        removeUrl,
        removeWikipediaLinks,
        removeRef,
        removeMath,
        removeOtherTags,
        removeHtmlFormat,
        removeOtherWikiFormat,
        removeUpperO,
        removeQuotationMark,
        removeEqual,
        removeBraces,
        removeBrackets,
        removeHtmlComment,
        removeAsterisk,
        removePx,
        removeDash,
        removeParentheses,
        removeDigits,
        removeOtherSymbols,
        removeWikipediaTemplates,
        removeRemainingBraces,
    ]
    x = text
    for func in funcs:
        x = func(x)
    return x


if __name__ == "__main__":
    data = []
    with open("dump_small.jsonln", "r") as file:
        for line in file:
            data.append(json.loads(line))

    with open("dump_small_clean.jsonln", "w", encoding="utf8") as file:
        for i in range(len(data)):
            json.dump(
                {"body": clearText(data[i]["body"]), "title": data[i]["title"]}, file
            )
            file.write("\n")
