import os

def build_toc():
    
    # get input and output folders, open each folder in directory, and make a toc for it

    inputFolder = "ReverseIndexes"
    outputFolder = "TableOfContents"

    os.makedirs(outputFolder, exist_ok = True)

    for file in os.listdir(inputFolder):
        filePath = os.path.join(inputFolder, file)
        
        if os.path.isfile(filePath):
            charName = os.path.splitext(file)[0]
            outputFileName = os.path.join(outputFolder, f"{charName}_toc.txt")

            currGroup = ''
            startByteOffset = -1
            byteOffset = 0

            # Open the input file for reading and the output file for writing
            with open(filePath, 'r') as inputFile:
                with open(outputFileName, 'w') as outputFile:
                    prevByteOffset = None  # track the previous line's byte offset for the end range
                    while True:
                        line = inputFile.readline()
                        if not line:
                            break
                        
                        # store the current byte offset at the start of the line
                        byteOffset = inputFile.tell() - len(line)  # get the position at the start of the line
                        
                        # split to get the token
                        token = line.split(':')[0]
                        tokenGroup = token[:2].lower()  # find the first two letters
                        
                        # if the letters have changed
                        if tokenGroup != currGroup:
                            if currGroup != '': 
                                # If it's not the previous group, write the range for the previous group
                                outputFile.write(f'"{currGroup}": [{startByteOffset}, {prevByteOffset}]\n')
                            
                            # Update the current group and start byte offset for the new letter
                            currGroup = tokenGroup
                            startByteOffset = byteOffset

                        # for the end range of the current letter
                        prevByteOffset = byteOffset
                    
                    # Handle the last group separately
                    if currGroup != '':
                        outputFile.write(f'"{currGroup}": [{startByteOffset}, {prevByteOffset}]\n')

def find_offset(token):

    findLetter = token[0].lower()
    tocFolder = "TableOfContents"
    tocFile = os.path.join(tocFolder,f"{findLetter}_toc.txt")
    startOffset = None
    endOffset = None

    with open(tocFile, 'r') as toc:
        for line in toc:
            # check for corresponding first 2 letters
            if line.strip().startswith(f'"{token[:2]}":'):
                # strip down toc formats to get start and ending range
                rangeString = line.split(':')[1].strip().strip('[]')
                rangeSplit = rangeString.split(',')
                
                startOffset = int(rangeSplit[0])
                endOffset = int(rangeSplit[1])
                break
    
    # return start and end lines as a list for easy use
    return [startOffset, endOffset]