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

# HELPERS FUNCTIONS
def extract_text(jsondict: dict) -> str:
    """
    Extracts HTML structured dictionary
    """
    html = bs(str(jsondict["content"]), "html.parser")
    text = (html.get_text()).replace("\\t"," ").replace("\\n"," ").replace("\\x"," ").replace("\\d"," ").replace("\\r"," ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def alphanumeric_check(char: str) -> bool:
    """
    Checks whether or not the char is an alphanumeric character. Used in the tokenizer function.
    """
    an = "abcdefghijklmnopqrstuvwxyz1234567890"
    if char.lower() not in an:
        return False
    return True

def tokenizer(text: str) -> defaultdict:
    """
    Takes in a string of text and tokenizes alphanumeric words. Returns a dictionary of the tokens and its frequency.
    A token is...
        - is alphanumeric
        - not a stop word
        - not less than 3 chars
    """
    tokens = defaultdict(list)
    token_start = None
    token_end = None
    token_string = ""
    prev_char = ""
    for i, char in enumerate(text):
        if alphanumeric_check(char):
            token_string += char
            if token_start == None:
                token_start = i
        elif alphanumeric_check(prev_char) == False and alphanumeric_check(char) == False:
            continue
        else:
            token_string = token_string.lower()
            token_end = i
            if (len(token_string) < 3):
                token_string = ""
                prev_char = char
                token_start = None
                token_end = None
                continue
            else:
                token_string = stemmer(token_string)
                if len(tokens[token_string]) == 0: #when it's empty
                    tokens[token_string].append(1) #[0]
                    tokens[token_string].append([]) #[1]
                    tokens[token_string][1].append(tuple([token_start, token_end])) 
                else:
                    tokens[token_string][1].append(tuple([token_start, token_end]))
                    tokens[token_string][0] += 1
            token_string = "" #reset
            token_start = None
            token_end = None
        prev_char = char 

    if (token_string != "") and (len(token_string) >= 3):
        token_string = stemmer(token_string)
        if len(tokens[token_string]) == 0: #when it's empty
            tokens[token_string].append(1) #[0]
            tokens[token_string].append([]) #[1]
            tokens[token_string][1].append(tuple([token_start, token_end])) 
        else:
            tokens[token_string][1].append(tuple([token_start, token_end]))
            tokens[token_string][0] += 1
    return tokens

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