# IMPORTS
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup as bs
from collections import defaultdict

# VARIABLES
stop_words = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren", "t", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "not", "cannot", "could",
    "couldn", "did", "didn", "do", "does", "doesn", "doing", "don", "down", "during", "each", "few", "for", "from",
    "further", "had", "hadn", "has", "hasn", "have", "haven", "having", "he", "d", "ll", "s", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "it", "its", "itself", "let", "me",
    "more", "most", "mustn", "my", "myself", "no", "nor", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan", "she", "should", "shouldn", "so", "some", "such",
    "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn", "we", "what", "when", "where", "which",
    "while", "who", "whom", "why", "with", "won", "would", "wouldn", "you", "your", "yours", "yourself", "yourselves"
]
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
    tokens = defaultdict(int)
    token_string = ""
    prev_char = ""
    for char in text:
        if alphanumeric_check(char):
            token_string += char
        elif alphanumeric_check(prev_char) == False and alphanumeric_check(char) == False:
            continue
        else:
            token_string = token_string.lower()
            if (token_string in stop_words) or (len(token_string) < 3):
                token_string = ""
                prev_char = char
                continue
            else:
                token_string = stemmer(token_string)
                tokens[token_string] += 1
            token_string = ""
        prev_char = char
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
