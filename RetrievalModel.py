# IMPORTS
import os
import json
import groupingTOC as GTOC
import ast
import helper_functions as hf

# VARIABLES
stop_words = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "arent", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "cant", "cannot", "could",
    "couldnt", "did", "didnt", "do", "does", "doesnt", "doing", "dont", "down", "during", "each", "few", "for", 
    "from", "further", "had", "hadnt", "has", "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", 
    "her", "here", "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im", 
    "ive", "if", "in", "into", "is", "isnt", "it", "its", "its", "itself", "lets", "me", "more", "most", 
    "mustnt", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", 
    "our", "ours", "ourselves", "out", "over", "own", "same", "shant", "she", "shed", "shell", "shes", 
    "should", "shouldnt", "so", "some", "such", "than", "that", "thats", "the", "their", "theirs", "them", 
    "themselves", "then", "there", "theres", "these", "they", "theyd", "theyll", "theyre", "theyve", 
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasnt", "we", "wed", 
    "well", "were", "weve", "were", "werent", "what", "whats", "when", "whens", "where", "wheres", 
    "which", "while", "who", "whos", "whom", "why", "whys", "with", "wont", "would", "wouldnt", "you", 
    "youd", "youll", "youre", "youve", "your", "yours", "yourself", "yourselves"
    ]

# MAIN FUNCTIONS
def process_query(query: str):

    """
    Uses the given AND boolean query in order to search for the top 5 related URLs.
    Returns a list of the top URLs.

    input:
        query: string -> the user query
    output:
        list -> top URLs
    """

    temp_tokens = query.split()
    tokens = []
    for t in temp_tokens:
        t = t.translate(hf.punctuation_table)
        t = t.lower()
        t = hf.porter_stemmer(t)
        if t in stop_words:
            continue
        tokens.append(t)
    print(tokens)

    tempDocIDs = []
    
    for token in tokens:
        tokenPostings = retrieve_tokenPostings(token)
        doc_ids = getDocIDs(tokenPostings)
        tempDocIDs.append(doc_ids)

    finalDocIDs = tempDocIDs[0]
    if len(tempDocIDs) > 1:
        for doc_ids in tempDocIDs[1:]:
            finalDocIDs = merge_two_doc(finalDocIDs, doc_ids)
            if not finalDocIDs:
                break

    finalDocURLs = getURLs(finalDocIDs)

    return finalDocURLs

# HELPER FUNCTIONS
def retrieve_tokenPostings(token):
    #tokenRange = GTOC.find_toc_range(token)

    with open("ReverseIndex.txt", 'r') as reverseIndex:
        for fileLine in reverseIndex:

            fileLine = fileLine.strip()
            currToken = fileLine.split(':')[0].strip()

            if token == currToken:
                # Safely evaluate the postings string
                postings = fileLine.split(':')[1].strip()
                return ast.literal_eval(postings)

    return []  # Return an empty list if token is not found in the reverse index

def getURLs(idList):
    '''
    Input: Document ID list
    Output: URL list corresponding to docIDs
    '''
    urls = []
    idListCopy = idList[:]
    with open("URL_Collective.txt", "r") as url_collection:
        row = 0
        for line in url_collection:
            row += 1
            for id in idListCopy:  # A COPY
                if row == int(id):
                    urls.append(line.strip())
                    idList.remove(id)
            if len(idList) == 0:
                break
    return urls

def getDocIDs(postings):
    """
    The postings parameter is the value
        - a key-value pair in the reverse index looks like:
            key = token : value = [p_1, ... , p_n]
        - a posting is:
            p = [docID, [tf-idf_score, {field_1, ..., field_n}]]
    The return value of this function is a list of docIDs for a word
    """
    docIDs = list()
    for p in postings:
        docIDs.append(p[0])
    return docIDs

def merge_two_doc(p1, p2):
    """
    Parameters: p1, p2
        - two SORTED DOCID postings
    Return Value: posting_result
        - an intersection of the two postings
    """
    posting_result = list()
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if int(p1[i]) == int(p2[j]):
            posting_result.append(int(p1[i]))
            i += 1
            j += 1
        elif int(p1[i]) < int(p2[j]):
            i += 1
        else:
            j += 1
    return posting_result

if __name__ == "__main__":
    #test_postings = [[123, [5.4, {'p', 'td'}]], [12314, [1.45, {'h1'}]], [3232, [2.2, {'p', 'strong'}]], [51, [3, {'title'}]], [3222, [2, {'p'}]]]
    #test_postings2 = ["cristal:[['27477', [8.75, {'p'}]]]", "crista:[['16903', [2.63, {'td'}]], ['16994', [2.63, {'h2'}]], ['19264', [2.63, {'p'}]], ['19419', [2.63, {'p'}]], ['19434', [2.63, {'p'}]], ['19460', [2.63, {'p'}]], ['21216', [2.63, {'li'}]], ['21222', [3.42, {'p'}]], ['21245', [3.42, {'p'}]], ['21399', [2.63, {'p'}]], ['21815', [5.14, {'p'}]], ['23073', [5.72, {'title', 'p', 'h3'}]], ['23387', [2.63, {'td'}]], ['24237', [3.42, {'p'}]], ['24569', [5.64, {'title', 'p', 'h3'}]], ['24650', [4.47, {'strong', 'p'}]], ['24822', [4.47, {'p'}]], ['25756', [2.63, {'li'}]], ['27066', [3.88, {'td', 'p'}]], ['27525', [3.42, {'td', 'p'}]], ['28112', [4.47, {'strong', 'p'}]], ['28262', [4.21, {'p'}]], ['28981', [5.47, {'p'}]], ['29118', [3.42, {'td', 'p'}]], ['29568', [4.21, {'p'}]], ['29691', [5.86, {'strong', 'p'}]], ['33348', [3.42, {'td'}]], ['33358', [5.72, {'title', 'p', 'h3'}]], ['33843', [3.42, {'h2', 'li'}]], ['34250', [5.64, {'title', 'p', 'h3'}]], ['34410', [3.42, {'td', 'p'}]], ['34683', [3.42, {'td', 'p'}]], ['34853', [4.21, {'li', 'p'}]], ['35143', [3.42, {'h2', 'li'}]], ['35147', [2.63, {'title'}]], ['36889', [3.88, {'strong', 'p'}]], ['37703', [3.88, {'td', 'p'}]], ['38521', [2.63, {'td'}]], ['40527', [3.42, {'p'}]], ['40849', [3.88, {'td', 'li', 'p'}]], ['41564', [5.64, {'p'}]], ['42502', [4.47, {'p'}]], ['43011', [4.21, {'p'}]], ['43460', [4.47, {'p'}]], ['43885', [4.21, {'p'}]], ['45012', [5.93, {'p'}]], ['45290', [5.0, {'p'}]], ['45368', [5.47, {'p'}]], ['45421', [3.88, {'p'}]], ['45620', [4.21, {'strong', 'p'}]], ['45779', [4.47, {'strong', 'p'}]], ['45815', [4.47, {'p'}]], ['45957', [5.47, {'p'}]], ['46563', [2.63, {'td'}]], ['47302', [2.63, {'p'}]], ['47928', [3.42, {'td', 'p'}]], ['48947', [5.0, {'strong', 'p'}]], ['49912', [4.68, {'strong', 'p'}]], ['50020', [5.0, {'p'}]], ['52944', [3.42, {'em', 'p'}]], ['53787', [3.42, {'strong', 'p'}]], ['53796', [3.42, {'strong', 'p'}]], ['53837', [3.42, {'strong', 'p'}]], ['53873', [2.63, {'li'}]], ['53875', [3.42, {'strong', 'p'}]], ['53999', [3.42, {'td'}]], ['54045', [2.63, {'p'}]], ['54692', [2.63, {'p'}]], ['54914', [2.63, {'p'}]]]]"

    # print(process_query("This is a test"))
    #print(f"Here is the {process_query('cristina lopes')}")
    #print(f"Here is the {process_query('machine learning')}")
    #print(f"Here is the {process_query('acm')}")
    #print(f"Here is the {process_query('master of software engineering')}")
    pass