# IMPORTS
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup as bs
from collections import defaultdict
from math import log

# VARIABLES
prefixes = [
    "a", "bi", "anti", "counter", "de", "dis", "extra", "fore", "in", "inter", "mal", "mis", "neo", "non", "over", "pre", 
    "post", "proto", "re", "sub", "tele", "trans", "tri", "un", "uni"
]
suffixes = [
    "able", "ant", "athon", "cide", "dom", "er", "ery", "ess", "esque", "ette", "fest", "fy", "hood", "ible", "ish", 
    "ism", "ist", "less", "ly", "ous", "wash"
]
htmltags = [
    "title", "p", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "li", "td", "th"
]
punctuation_table = {
    ord("!"): None, ord("'"): None, ord(","): None, ord("-"): None, ord("."): None, 
    ord(":"): None, ord(";"): None, ord("?"): None, ord("_"): None, ord("`"): None
}

# HELPERS FUNCTIONS
def alphanumeric_check(char: str) -> bool:
    """
    Checks whether or not the char is an alphanumeric character. Used in the tokenizer function.
    """
    an = "abcdefghijklmnopqrstuvwxyz1234567890"
    if char.lower() not in an:
        return False
    return True

def stemmer(text: str) -> str:
    """
    Takes in a string of text and removes any prefixes/suffixes. Returns the string in its base form.
    It will not parse words if removing any suffixes/prefixes makes it too short.
    """
    new_word = text
    for prefix in prefixes:
        if (text.startswith(prefix) and (len(text.removeprefix(prefix)) >= 5)):
            new_word = new_word.removeprefix(prefix)
    for suffix in suffixes:
        if (text.endswith(suffix) and (len(text.removesuffix(prefix)) >= 5)):
            new_word = new_word.removesuffix(suffix)
    return new_word

def defrag_url(url: str) -> str:
    """
    Given a url as a string, it returns that url without its fragments.
    """
    parsed_url = urlparse(url)
    defragged_url = urlunparse(parsed_url._replace(fragment=""))
    return defragged_url

def tfidf(freq: int, docfreq: int) -> float:
    """
    Weight formula for TF-IDF:
    w(x,y) = tf(x,y) * log(N/df(x))
        - tf(x,y) = freq of x in y
        - df(x) = # of documents containing x
        - N = total # of documents
    """
    # TODO: NEED to REFACTOR for actual use
    n = input("input for # of docs") # TODO: <== N is the total number of documents
    temp = n/docfreq
    return round(freq * log(temp), 2)

def extract_tokenize_fields(jsondict: dict) -> defaultdict:
    """
    An updated version tokenizer that also extracts text. This tokenizer will also record the fields of each token.

    Data in the dictionary(k:v):
        token <str> : [freq <int>, {field <str>, ..., n} <set>]<list>
    """
    tokens = defaultdict(list)
    html = bs(str(jsondict["content"]), "html.parser")
    for e in html.find_all(htmltags):
        tag = e.name
        text = (e.get_text()).replace("\\t"," ").replace("\\n"," ").replace("\\x"," ").replace("\\d"," ").replace("\\r"," ")
        words = text.split()
        for word in words:
            word = word.translate(punctuation_table)
            if not is_valid_token(word):
                continue
            word = word.lower()
            #word = stemmer(word)
            if len(tokens[word]) == 0:
                tokens[word].append(1)
                tokens[word].append(set())
                tokens[word][1].add(tag)
            else:
                tokens[word][0] += 1
                tokens[word][1].add(tag)
    return tokens

def is_valid_token(token: str) -> bool:
    """
    Checks whether the string provided is a valid token:
        - is alphanumeric_check
        - 
    """
    if len(token) < 3:
        return False
    for char in token:
        if alphanumeric_check(char):
            continue
        else:
            return False
    return True
