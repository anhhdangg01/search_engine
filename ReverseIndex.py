import os
import json
import groupingTOC as GTOC
import helper_functions as hf
from collections import defaultdict
import ast
from bs4 import BeautifulSoup

numTempFile = 0
tempIndex = {}

def countNumofDoc():
    '''
    Returns the number of urls processed by the tool.
    '''
    sol = 0
    with open("URL_Collective.txt") as file:
        for line in file:
            sol+=1

    return sol


def buildTF_IDF(totalNumDoc):

    '''
    
    This iterates through the MergedList (proto-reverse-index based on frequency) and calculates the TF-IDF score.
    Then it replaces the frequency count with the TF-IDF and builds a new list, named ReverseIndex.txt.
    
    '''
    with open(os.getcwd() + "/TempFiles/MergedList.txt",'r') as PreProcessedList, open("ReverseIndex.txt",'w') as ReverseIndex:
            wordlist = PreProcessedList.readline().strip()
            while(wordlist):
                key, value = wordlist.split(":", 1)
                postingsList = ast.literal_eval(value)
                numDoc = len(postingsList)
                postPostingsList = []
                for freq in postingsList:     
                    tf_idfScore = hf.tfidf(int(freq[1][0]),numDoc,totalNumDoc)
                    freq[1][0] = tf_idfScore
                    postPostingsList.append(freq)

                #print(postPostingsList)
                ReverseIndex.write(f"{key}:{postPostingsList}\n")
                wordlist = PreProcessedList.readline()
    

def Archieve_URL(url, DocumentID):
    '''
    This appends the URL to URL_Collective.txt.
    It creates a history of the processed URL. 
    '''
    with open("URL_Collective.txt", "a") as file:
        file.write(url+"\n")


def clear_line_in_file(file_path, line_to_clear):
    '''
    (Depreciated) replaces the original file with a copy of the original file with edits. 
    '''
    temp_file_path = 'temp_' + file_path
    with open(file_path, 'r') as original_file, open(temp_file_path, 'w') as temp_file:
        for current_line_number, line in enumerate(original_file):
            if current_line_number != line_to_clear:
                temp_file.write(line)  # Write all lines except the one to be removed

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)


def get_Index(token):
    '''
    (Depreciated) gets the row that contains postings in the temp reverse index given a token. 
    '''
    lineNum = 0
    with open("ReverseIndex.txt", "r") as file:
        for line in file:
            Index = json.loads(line)
            if token in Index:
                #remove that line from the .txt file and move everything up without loading everything into memory.
                clear_line_in_file("ReverseIndex.txt", lineNum)
                return Index
            lineNum+=1
    return {}

def CreateIndex(DocumentID, tokens):
    '''
    Given a document ID and tokens, it will iterate through the tokens and append them to the tempIndex.
    If the length of the temp index exceeds length of 50, it will offload it to a temporary partial index. 
    Upon termination, it will offload the rest of the tempIndex into a temporary partial index.
    '''
    global numTempFile
    global tempIndex
    

    for tuple_Entry in tokens:
        if(len(tempIndex) <= 50):
            #add it into the curr temp list
            
            if(str(tuple_Entry[0]) in tempIndex):
                #update the index

                Token_Entry = [str(DocumentID), tuple_Entry[1]]
                tempIndex[tuple_Entry[0]].append(Token_Entry)

            else:
                Token_Entry = [str(DocumentID), tuple_Entry[1]]
                tempIndex[str(tuple_Entry[0])] = [Token_Entry]

        else:
            if(str(tuple_Entry[0]) in tempIndex):
                #update the index

                Token_Entry = [str(DocumentID), tuple_Entry[1]]
                tempIndex[tuple_Entry[0]].append(Token_Entry)

            else:
                Token_Entry = [str(DocumentID), tuple_Entry[1]]
                tempIndex[str(tuple_Entry[0])] = [Token_Entry]
                
            #dump content into a temp file. 
            tempIndex = dict(sorted(tempIndex.items()))
            with open(os.getcwd() + "/TempFiles/"+ str(numTempFile) + ".txt", "a") as file:
                for token,value in tempIndex.items():
                    file.write(token+":["+(','.join(map(str, value)))+"]\n")
            numTempFile+=1
            tempIndex = {}




def countTokens():
    '''
    Returns the number of unique tokens in the MergedList.txt file (i.e combination of all partial reverse indexes.)
    '''
    tempWorkingDir = os.getcwd() + "/TempFiles/"
    mergeListPath = tempWorkingDir + "MergedList.txt"

    NumberofUniqueTokens = 0

    with open (mergeListPath, 'r') as CoaleasedFile:
        for line in CoaleasedFile:
            NumberofUniqueTokens+=1

    with open (tempWorkingDir + "TotalUniqueTokens.txt", 'w') as TotalTokenCount:
        TotalTokenCount.write("Total Number of Unique Tokens: " + str(NumberofUniqueTokens))


def merge_two_files(file1_path, file2_path, output_path):
    '''
    Helper function to merge two sorted files into one.
    '''
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2, open(output_path, 'w') as output_file:
        line1 = file1.readline().strip()
        line2 = file2.readline().strip()

        while line1 or line2:
            if not line1:
                output_file.write(line2 + "\n")
                line2 = file2.readline().strip()
            elif not line2:
                output_file.write(line1 + "\n")
                line1 = file1.readline().strip()
            else:
                key1, value1 = line1.split(":", 1)
                key2, value2 = line2.split(":", 1)

                if key1 < key2:
                    output_file.write(line1 + '\n')
                    line1 = file1.readline().strip()
                elif key1 > key2:
                    output_file.write(line2 + '\n')
                    line2 = file2.readline().strip()
                else:
                    list1 = ast.literal_eval(value1)
                    list2 = ast.literal_eval(value2)
                    merged_value = list1 + list2
                    output_file.write(f"{key1}:{merged_value}\n")
                    line1 = file1.readline().strip()
                    line2 = file2.readline().strip()


def merge_files_iteratively(numTempFile):
    '''
    Given a list of temporary partial indexes, it pairs them in a alternating pattern and merges them.
    This technique lowers the number of comparisons needed to merge all of the files. 
    '''
    tempWorkingDir = os.getcwd() + "/TempFiles/"
    
    # Initial list of files to merge
    files_to_merge = [tempWorkingDir + f"{i}.txt" for i in range(numTempFile)]
    merge_round = 1

    while len(files_to_merge) > 1:
        print(f"Merging Round {merge_round}: {len(files_to_merge)} files to merge.")
        new_files = []

        # Process files in pairs
        for i in range(0, len(files_to_merge), 2):
            file1 = files_to_merge[i]
            
            if i + 1 < len(files_to_merge):
                file2 = files_to_merge[i + 1]
                merged_file_path = tempWorkingDir + f"merged_{merge_round}_{i // 2}.txt"
                merge_two_files(file1, file2, merged_file_path)
                new_files.append(merged_file_path)
                
                # Optionally delete intermediate files
                os.remove(file1)
                os.remove(file2)
            else:
                # If there's an odd file out, carry it to the next round
                new_files.append(file1)

        # Update the list of files to merge in the next round
        files_to_merge = new_files
        merge_round += 1

    # The last remaining file is the fully merged output
    final_merged_file = files_to_merge[0]
    print(f"Final merged file: {final_merged_file}")
    os.rename(final_merged_file, tempWorkingDir + "MergedList.txt")


def initialize_Reverse_Index_Process():
    '''
    Main function. Recursively gets all files from the "Sites" folder and tokenizes them before inserting it into the reverse index.
    
    Afterward, it will calculate the TF-IDF using "MergedList.txt" (i.e a combination of all partial reverse indexes.) and output a final
    reverse index, "ReverseIndex.txt".
    '''
    global tempIndex
    global numTempFile
    DocumentID = 1
    tokens = [] #remove this comment

    #CALL SIMILARTY FUNCTION HERE:
        #IF SIMILAR continue. 


    dir_path = os.getcwd() + "/Sites"

    '''
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root,file)

                with open(file_path,'r') as f:
                    try:
                        data = json.load(f)
                        url = hf.defrag_url(data.get("url"))
                        tokens = hf.extract_tokenize_fields(data)

                        #CALL SIMILARTY FUNCTION HERE:
                            #IF SIMILAR continue. 
                        
                        Archieve_URL(url, DocumentID)
                        CreateIndex(DocumentID, list(tokens.items()))

                        DocumentID+=1
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")

    if(len(tempIndex)!=0):
        tempIndex = dict(sorted(tempIndex.items()))
        with open(os.getcwd() + "/TempFiles/"+ str(numTempFile) + ".txt", "a") as file:
            for token,value in tempIndex.items():
                file.write(token+":["+(','.join(map(str, value)))+"]\n")
        numTempFile+=1
        tempIndex = {}


    
    merge_files_iteratively(numTempFile)
    countTokens()
    #recursiveMerge() #:( SAD CODE RIGHT HERE <-
    #GTOC.group_reverse_index()
    
    GTOC.build_toc(os.getcwd() + "/TempFiles/MergedList.txt")
    '''
    totalNumDoc = countNumofDoc()
    buildTF_IDF(totalNumDoc)




def test_one_folder():
    curdir = os.getcwd()
    target = os.path.join(curdir, "DEV", "aiclub_ics_uci_edu")
    if os.path.exists(target) and os.path.isdir(target):
        for file in os.listdir(target):
            if file.endswith(".json"):
                path = os.path.join(target, file)
                with open(path, "r") as jsonf:
                    data = json.load(jsonf)
                    x = hf.extract_tokenize_fields(data)
                    #text = hf.extract_text(data)
                    #token_dict = hf.tokenizer(text)

                    
if __name__ == "__main__":
    #test_one_folder
    initialize_Reverse_Index_Process()
