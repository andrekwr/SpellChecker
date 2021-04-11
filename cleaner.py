import json
import re


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


def removeWikipediaLinks(text):
    pattern = r"\[\[(?:[^|]*?\|)*?([^|]*?)\]\]"
    repl = r"\1"
    matcher = re.compile(pattern)
    return matcher.sub(repl, text)


def removeRef(text):
    return re.sub(r"<ref(?:.*)?>.*?(?:</ref>)?", "", text)


def removeMath(text):
    return re.sub(r"<math(?:.*)?>.*?(?:</math>)?", "", text)


def removeOtherTags(text):
    return re.sub(r"<.*?>(.*?)<.*?>", r"\1", text)


def removeHtmlFormat(text):
    return re.sub(r'\w+=".*"', "", text)


def removeOtherWikiFormat(text):
    return re.sub(r"\w+=.+", " ", text)


def removeQuotationMark(text):
    pattern = r"""(['"]+)(.*?)\1"""
    matcher = re.compile(pattern)
    return matcher.sub(r"\2", text)


def removeEqual(text):
    return text.replace("=", " ")


def removeBraces(text):
    pattern = r"{.*?}"
    matcher = re.compile(pattern)
    return matcher.sub("", text)


def removeBrackets(text):
    pattern = r"\[.*?\]"
    matcher = re.compile(pattern)
    text = matcher.sub("", text)
    text = text.replace("]", "")
    return text.replace("[", "")


def removeHtmlComment(texto):
    pattern = r"<!--.*?-->"
    matcher = re.compile(pattern)
    return matcher.sub("", texto)


def removeAsterisk(texto):
    texto = texto.replace("*", "")
    return texto


def removePx(text):
    return re.sub(r"(?:\d+x)?\d+px", " ", text)


def removeDash(text):
    return re.sub(r"\s+[-–]\s+", " ", text)


def removeParentheses(text):
    text = text.replace("(", "")
    return text.replace(")", "")


def removeUpperO(text):  # °
    return text.replace("\u00ba", "")


def removeDigits(text):
    return re.sub("\d+", "", text)


def removeOtherSymbols(text):
    toRemove = ["|", ",", "\n", "\t", ";"]
    x = text
    for i in toRemove:
        x.replace(i, "")
    return x


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
