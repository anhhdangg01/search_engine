# IMPORTS


# VARIABLES


# MAIN FUNCTIONS
def retrieve_docs(query: str) -> list:
    """
    Uses the given AND boolean query in order to search for the top 5 related URLs.
    Returns a list of the top URLs.

    input:
        query: string -> the user query
    ouput:
        list -> top URLs

    """
    urls = []
    query_index = {}
    bigrams = create_bigrams(query)
    tokens = query.split()
    query_postings = []

    for token in tokens:
        first_str = token[0]
        query_index[first_str] = find_toc_range(token)

    with open("ReverseIndex.txt") as reverse_indexes:
        reverse_indexes_content = reverse_indexes.readlines()
        for token in tokens:
            postings = []
            first_str = token[0]
            index = query_index[first_str][0]
            while index <= query_index[first_str][1]:
                line = reverse_indexes_content[index].split(":")
                if line[0] == token:
                    print(line[0])
                    postings.append(line[1])
                index += 1
            query_postings.append(postings)
            
    # return postings

    # convert posting strings into actual data structure here
    docIDs = []
    for posting in query_postings:
        docIDs.append(sorted(getDocIDs(posting)))
    while len(docIDs) > 1:
        docIDs[0] = merge_two_doc(docIDs[0], docIDs[1])
    for doc in docIDs[0]:
        # find the URLs in URL_Collective.txt using docIDs, then append them to urls
        continue #stub

    return urls

# HELPER FUNCTIONS
def getDocIDs(postings):
    """
    The postings parameter is the value
        - a key value pair in the reverse index looks like:
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
        - a intersection of the two postings
    """
    posting_result = list()
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            posting_result.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
    return posting_result

def create_bigrams(text: str) -> list:
    """
    Takes in a string of text and breaks it up into a boolean query on bigrams.

    input:
        text: string -> a sequence of characters
    output:
        list -> bigrams of text

    """
    k = 2
    kgrams = []
    words = text.split()

    for word in range(len(words) - k + 1):
        kgrams.append(" ".join(words[word:word + k]))
    
    return kgrams

def find_toc_range(token):

    findLetter = token[0].lower()
    inputFile = "TableOfContents.txt"
    startLine = None
    endLine = None

    with open(inputFile, 'r') as toc:
        for line in toc:
            # Check each line for the corresponding first letter
            if line.strip().startswith(f'"{findLetter}":'):
                # Strip down toc formats to get start and ending range
                range_str = line.split(':')[1].strip().strip('[]')
                rangeSplit = range_str.split(',')
                startLine = int(rangeSplit[0])
                endLine = int(rangeSplit[1])
                break

    return [startLine, endLine]


if __name__ == "__main__":
    test_postings = [[123, [5.4, {'p', 'td'}]], [12314, [1.45, {'h1'}]], [3232, [2.2, {'p', 'strong'}]], [51, [3, {'title'}]], [3222, [2, {'p'}]]]
    test_postings2 = ["cristal:[['27477', [8.75, {'p'}]]]", "crista:[['16903', [2.63, {'td'}]], ['16994', [2.63, {'h2'}]], ['19264', [2.63, {'p'}]], ['19419', [2.63, {'p'}]], ['19434', [2.63, {'p'}]], ['19460', [2.63, {'p'}]], ['21216', [2.63, {'li'}]], ['21222', [3.42, {'p'}]], ['21245', [3.42, {'p'}]], ['21399', [2.63, {'p'}]], ['21815', [5.14, {'p'}]], ['23073', [5.72, {'title', 'p', 'h3'}]], ['23387', [2.63, {'td'}]], ['24237', [3.42, {'p'}]], ['24569', [5.64, {'title', 'p', 'h3'}]], ['24650', [4.47, {'strong', 'p'}]], ['24822', [4.47, {'p'}]], ['25756', [2.63, {'li'}]], ['27066', [3.88, {'td', 'p'}]], ['27525', [3.42, {'td', 'p'}]], ['28112', [4.47, {'strong', 'p'}]], ['28262', [4.21, {'p'}]], ['28981', [5.47, {'p'}]], ['29118', [3.42, {'td', 'p'}]], ['29568', [4.21, {'p'}]], ['29691', [5.86, {'strong', 'p'}]], ['33348', [3.42, {'td'}]], ['33358', [5.72, {'title', 'p', 'h3'}]], ['33843', [3.42, {'h2', 'li'}]], ['34250', [5.64, {'title', 'p', 'h3'}]], ['34410', [3.42, {'td', 'p'}]], ['34683', [3.42, {'td', 'p'}]], ['34853', [4.21, {'li', 'p'}]], ['35143', [3.42, {'h2', 'li'}]], ['35147', [2.63, {'title'}]], ['36889', [3.88, {'strong', 'p'}]], ['37703', [3.88, {'td', 'p'}]], ['38521', [2.63, {'td'}]], ['40527', [3.42, {'p'}]], ['40849', [3.88, {'td', 'li', 'p'}]], ['41564', [5.64, {'p'}]], ['42502', [4.47, {'p'}]], ['43011', [4.21, {'p'}]], ['43460', [4.47, {'p'}]], ['43885', [4.21, {'p'}]], ['45012', [5.93, {'p'}]], ['45290', [5.0, {'p'}]], ['45368', [5.47, {'p'}]], ['45421', [3.88, {'p'}]], ['45620', [4.21, {'strong', 'p'}]], ['45779', [4.47, {'strong', 'p'}]], ['45815', [4.47, {'p'}]], ['45957', [5.47, {'p'}]], ['46563', [2.63, {'td'}]], ['47302', [2.63, {'p'}]], ['47928', [3.42, {'td', 'p'}]], ['48947', [5.0, {'strong', 'p'}]], ['49912', [4.68, {'strong', 'p'}]], ['50020', [5.0, {'p'}]], ['52944', [3.42, {'em', 'p'}]], ['53787', [3.42, {'strong', 'p'}]], ['53796', [3.42, {'strong', 'p'}]], ['53837', [3.42, {'strong', 'p'}]], ['53873', [2.63, {'li'}]], ['53875', [3.42, {'strong', 'p'}]], ['53999', [3.42, {'td'}]], ['54045', [2.63, {'p'}]], ['54106', [2.63, {'p'}]], ['54112', [2.63, {'li'}]], ['54128', [2.63, {'li'}]], ['54129', [3.42, {'strong', 'p'}]], ['54135', [3.88, {'h2', 'title', 'p'}]], ['54160', [3.88, {'h2', 'title', 'p'}]], ['54171', [2.63, {'p'}]], ['54172', [3.42, {'strong', 'p'}]], ['54174', [2.63, {'p'}]], ['54184', [2.63, {'p'}]], ['54186', [3.42, {'strong', 'p'}]], ['54191', [3.42, {'strong', 'p'}]], ['54197', [3.42, {'strong', 'p'}]], ['54289', [2.63, {'td'}]], ['54309', [3.88, {'h2', 'title', 'p'}]], ['54310', [3.42, {'h2', 'p'}]], ['54317', [2.63, {'p'}]], ['54344', [3.42, {'h2', 'p'}]], ['54348', [3.42, {'h2', 'p'}]], ['54351', [2.63, {'p'}]], ['54361', [3.42, {'p'}]], ['54369', [3.42, {'strong', 'p'}]], ['54370', [3.42, {'strong', 'p'}]], ['54378', [2.63, {'p'}]], ['54424', [3.42, {'strong', 'p'}]], ['54487', [2.63, {'td'}]], ['54519', [3.42, {'p'}]], ['54529', [3.42, {'strong', 'p'}]], ['54570', [2.63, {'p'}]], ['54592', [2.63, {'p'}]], ['54644', [2.63, {'li'}]], ['54670', [3.42, {'h2', 'p'}]], ['54672', [2.63, {'p'}]], ['54677', [2.63, {'p'}]], ['54689', [3.42, {'h2', 'p'}]], ['54727', [2.63, {'p'}]], ['54771', [2.63, {'li'}]], ['54788', [2.63, {'li'}]], ['54793', [3.42, {'strong', 'p'}]], ['54798', [3.42, {'h2', 'p'}]], ['54804', [2.63, {'p'}]], ['54815', [2.63, {'p'}]], ['54817', [2.63, {'p'}]], ['54828', [3.42, {'p'}]], ['54830', [3.42, {'td'}]], ['54870', [3.42, {'strong', 'p'}]], ['54906', [2.63, {'p'}]], ['54912', [3.42, {'p'}]], ['54938', [2.63, {'p'}]], ['54963', [3.88, {'h2', 'title', 'p'}]], ['55033', [3.42, {'p'}]], ['55046', [3.42, {'strong', 'p'}]], ['55069', [3.42, {'strong', 'p'}]], ['55075', [3.42, {'p'}]], ['55108', [2.63, {'p'}]], ['55154', [2.63, {'p'}]], ['55185', [2.63, {'p'}]], ['55194', [2.63, {'p'}]], ['55245', [2.63, {'li'}]], ['55248', [3.42, {'p'}]], ['55256', [2.63, {'p'}]], ['55328', [3.42, {'p'}]], ['55384', [2.63, {'li'}]]]"]
    # test_p1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # test_p2 = [3, 6, 7, 9, 10, 11, 12]
    # print(getDocIDs(test_postings))
    # print(merge_two_doc(test_p1, test_p2))
    # print(":o)")
    # print(create_bigrams("master of software engineering"))
    print(retrieve_docs("cristal lopesdecember"))