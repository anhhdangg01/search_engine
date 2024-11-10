import json
import os
from collections import defaultdict

def group_reverse_index (inputFile = "ReverseIndex.txt"):
    # grouped token list
    #groupedIndex = defaultdict(list)

    os.makedirs('TOC', exist_ok=True)

    #open and read line by line
    with open(inputFile, 'r') as file:
        for line in file:
            element = json.loads(line.strip()) 

            for token, values in element.items():
                tokenLetter = token[0].lower() #First letter

                #write token information into temp file (first letter)
                tempFileName = f'TOC/{tokenLetter}.txt' 
                with open (tempFileName, 'a') as tempFile:
                    tempEntry = json.dumps({token: values})
                    tempFile.write(tempEntry + "\n")

    #os.makedirs('GroupedReverse.txt')

    #Create output file using GroupedIndex
    outputFileName = 'GroupedReverse.txt'
    with open(outputFileName, 'w') as outputFile:
        for tempLetter in os.listdir('TOC'):
            tempFileName = f'TOC/{tempLetter}'
    
            with open(tempFileName, 'r') as tempFile:
                for tokenLine in tempFile:
                    outputFile.write(tokenLine)

    for tempFileName in os.listdir('TOC'):
        os.remove(f'TOC/{tempFileName}')
    
    os.rmdir('TOC')

group_reverse_index()

def build_toc (inputFile = "GroupedReverse.txt"):
    
    currLetter = ''
    startLine = -1
    lineIndex = 0
    outputFileName = 'TableOfContents.txt'
    # Read the input file
    with open(inputFile, 'r') as inputFile:
        with open(outputFileName, 'w') as outputFile:
            for line in inputFile:
                lineIndex += 1

                element = json.loads(line.strip())
                token = list(element.keys())[0]
                tokenLetter = token[0].lower()

                if tokenLetter != currLetter:
                    if currLetter != '':
                        outputFile.write(f'"{currLetter}": [{startLine}, {lineIndex-1}]\n')
                    
                    currLetter = tokenLetter
                    startLine = lineIndex
                    
            if currLetter != '':
                outputFile.write(f'"{currLetter}": [{startLine}, {lineIndex}]\n')

build_toc()