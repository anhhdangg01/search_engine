# IMPORTS


# VARIABLES


# MAIN FUNCTIONS


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

if __name__ == "__main__":
    # test_postings = [[123, [5.4, {'p', 'td'}]], [12314, [1.45, {'h1'}]], [3232, [2.2, {'p', 'strong'}]], [51, [3, {'title'}]], [3222, [2, {'p'}]]]
    # test_p1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # test_p2 = [3, 6, 7, 9, 10, 11, 12]
    # print(getDocIDs(test_postings))
    # print(merge_two_doc(test_p1, test_p2))
    print(":o)")
