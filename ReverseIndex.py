import os
import json
import groupingTOC as GTOC
import helper_functions as hf
from collections import defaultdict
import ast

numTempFile = 0
tempIndex = {}

def create_Index_TOC(indexes):
    with open("ReverseIndex.txt", "rw") as file:
        raw_Index = file.readline.strip()
        indexes = json.loads(raw_Index)
    

def Archieve_URL(url, DocumentID):
    with open("URL_Collective.txt", "a") as file:
        file.write(url+"\n")


def clear_line_in_file(file_path, line_to_clear):
    temp_file_path = 'temp_' + file_path
    with open(file_path, 'r') as original_file, open(temp_file_path, 'w') as temp_file:
        for current_line_number, line in enumerate(original_file):
            if current_line_number != line_to_clear:
                temp_file.write(line)  # Write all lines except the one to be removed

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)


def get_Index(token):
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
            #dump content into a temp file. 
            tempIndex = dict(sorted(tempIndex.items()))
            with open(os.getcwd() + "/TempFiles/"+ str(numTempFile) + ".txt", "a") as file:
                for token,value in tempIndex.items():
                    file.write(token+":["+(','.join(map(str, value)))+"]\n")
            numTempFile+=1
            tempIndex = {}

    if(len(tempIndex)!=0):
        tempIndex = dict(sorted(tempIndex.items()))
        with open(os.getcwd() + "/TempFiles/"+ str(numTempFile) + ".txt", "a") as file:
            for token,value in tempIndex.items():
                file.write(token+":["+(','.join(map(str, value)))+"]\n")
        numTempFile+=1
        tempIndex = {}





    '''
    for tuple_Entry in tokens:
        Index = get_Index(tuple_Entry[0])        #check through the list of tokens in the file.
    
        if (len(Index) != 0):
            totalFreq = 0
            #it exists, update it.
                #If updating, no need to update the index. 


            Token_Entry = [str(DocumentID), tuple_Entry[1]]
            Index[str(tuple_Entry[0])].append(Token_Entry)
            Index[str(tuple_Entry[0])][0][1] += tuple_Entry[1]

            for key, value in Index.items():
                Index[key] = sorted(value, key=lambda x: list(x), reverse=True)   #This sorts by file ID. 

            with open("ReverseIndex.txt", "a") as file:
                file.write(json.dumps(Index)+"\n")



        else:
            #Append it.
            #If appending. Update the index. 

            Token_Entry = [str(DocumentID), tuple_Entry[1]]
            TotalFreq_Entry = ["Total", tuple_Entry[1]]
            Index[tuple_Entry[0]] = [TotalFreq_Entry, Token_Entry]



            with open("ReverseIndex.txt", "a") as file:
                file.write(json.dumps(Index)+"\n")
    '''

def recursiveMerge():
    global numTempFile
    tempWorkingDir = os.getcwd() + "/TempFiles/"
    mergeListPath = tempWorkingDir + "MergedList.txt"
    temp_file_path = tempWorkingDir + "temp_MergedList.txt"

    for i in range (0, numTempFile):
        currMergeItmPath = tempWorkingDir + str(i) + ".txt" #back to run it on openlab.
        print("CURR READING: " + currMergeItmPath)
        
    
        with open (currMergeItmPath, 'r') as targetmerge, open (mergeListPath, 'r') as CoaleasedFile, open(temp_file_path, 'w') as temp_file:
            
            
            mergeItm = targetmerge.readline().strip()
            coaleasedItm = CoaleasedFile.readline().strip()
        
            while mergeItm or coaleasedItm:
                if not mergeItm:
                    temp_file.write(coaleasedItm+"\n")
                    coaleasedItm = CoaleasedFile.readline().strip()
                elif not coaleasedItm:
                    temp_file.write(mergeItm+"\n")
                    mergeItm = targetmerge.readline().strip()
                else:

                    key1,value1 = mergeItm.split(":",1)
                    key2,value2 = coaleasedItm.split(":",1)

                    if key1 < key2:
                        temp_file.write(mergeItm + '\n')
                        mergeItm = targetmerge.readline().strip()
                    elif key1 > key2:
                        temp_file.write(coaleasedItm + '\n')
                        coaleasedItm = CoaleasedFile.readline().strip()
                    else:

                        
                        list1 = ast.literal_eval(value1)
                        list2 = ast.literal_eval(value2)

                        merged_value = list1 + list2

                        
                        temp_file.write(f"{key1}:{merged_value}\n")

                        mergeItm = targetmerge.readline().strip()
                        coaleasedItm = CoaleasedFile.readline().strip()

            
            os.replace(temp_file_path, mergeListPath)






def initialize_Reverse_Index_Process():
    DocumentID = 1
    tokens = [] #remove this comment

    #CALL SIMILARTY FUNCTION HERE:
        #IF SIMILAR continue. 


    dir_path = os.getcwd() + "/Sites"

    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root,file)

                with open(file_path,'r') as f:
                    try:
                        data = json.load(f)
                        url = data.get("url")

                        #tokenize data here.

                        tokens = hf.tokenizer(hf.extract_text(data))

                        #CALL SIMILARTY FUNCTION HERE:
                            #IF SIMILAR continue. 
                        
                        Archieve_URL(url, DocumentID)
                        CreateIndex(DocumentID, list(tokens.items()))
                        DocumentID+=1
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")


    
    recursiveMerge() #:( SAD CODE RIGHT HERE <-
    #GTOC.group_reverse_index()

# TEST METHOD
def test_one_folder():
    curdir = os.getcwd()
    target = os.path.join(curdir, "DEV", "aiclub_ics_uci_edu")
    if os.path.exists(target) and os.path.isdir(target):
        for file in os.listdir(target):
            if file.endswith(".json"):
                path = os.path.join(target, file)
                with open(path, "r") as jsonf:
                    data = json.load(jsonf)
                    text = hf.extract_text(data)
                    token_dict = hf.tokenizer(text)
                    print(token_dict)
                    print()

if __name__ == "__main__":
    test_one_folder()
    #initialize_Reverse_Index_Process()
