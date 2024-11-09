import os
import json
import helper_functions as hf


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

def IndexAppendORUpdate(DocumentID, tokens):
    #indexes = {}
    #get_index_TOC(indexes)

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




def initialize_Reverse_Index_Process():
    DocumentID = 1
    tokens = [("TEST1", 12),("AAAAA",3),("AAAAA",38),("AAAAA",25),("TEST5", 12)] #SAMPLE CALL
    #tokens = [] #remove this comment

    #CALL SIMILARTY FUNCTION HERE:
    #IF SIMILAR continue. 

    Archieve_URL("TESTLINK.com", DocumentID)#SAMPLE CALL
    IndexAppendORUpdate(DocumentID, tokens)#SAMPLE CALL
    DocumentID+=1#SAMPLE CALL

    Archieve_URL("TESTLINK2.com", DocumentID)#SAMPLE CAL
    IndexAppendORUpdate(DocumentID, tokens)#SAMPLE CALL
    DocumentID+=1#SAMPLE CALL



    #remove this block comment and delete the sample calls when the tokenize function is implemented. 
    '''
    for root, _, files in os.walk(""):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root,file)

                with open(file_path,'r') as f:
                    try:
                        data = json.load(f)
                        url = data.get("url")

                        #tokenize data here.

                        tokens = [("TEST1", 12),("AAAAA",3)]

                        #CALL SIMILARTY FUNCTION HERE:
                            #IF SIMILAR continue. 

                        Archieve_URL(url, DocumentID)
                        IndexAppendORUpdate(DocumentID, tokens)
                        DocumentID+=1



                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")
    '''

# EASY TEST METHOD
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



if __name__ == "__main__":
<<<<<<< Updated upstream
    initialize_Reverse_Index_Process()
=======
    test_one_folder()
    #initialize_Reverse_Index_Process()
>>>>>>> Stashed changes
