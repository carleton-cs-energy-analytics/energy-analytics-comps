import sys
import csv
import json

def main():
    # Read in csv and store the contents into "fileContents"
    with open(sys.argv[1], 'rU') as csvFile:
        fileReader = csv.reader(csvFile)
        fileContents = list(fileReader)
    
    oldFormat = False
    newList = []
    if (oldFormat):
        # Remove empty lines and removes spaces
        newList = [line[0].strip() for line in fileContents if len(line) > 0]
    else:
        # Same thing but for a different output format
        combLine = []
        for line in fileContents:
            if (len(line) > 0):
               if (len(line) > 1):
                   newList.append(line[0].strip() + " " + line[1].strip())
               else:
                   newList.append(line[0].strip())
    
    
    baseJsonDict = {}
    index = 0;
    while (index < len(newList)):
    
        # If we are about to start a new point:
        if (newList[index].startswith("Point System Name")):
            dictToAppend = {}
            memEntry = None;
            
            # Set the name of the point as the key to a new entry
            baseJsonDict[newList[index].split(':', 1)[1].strip()] = dictToAppend
            index += 1
            
            # While we are still parsing the same point:
            while (not ((newList[index] == '') or (newList[index].startswith("******")))):
                splitString = newList[index].split(':', 1)
                
                # If the string has two points add them both into the dictionary:
                if (len(splitString) != 1):
                    dictToAppend[splitString[0]] = splitString[1].strip()
                    memEntry = (splitString[0], dictToAppend[splitString[0]], True);
                    
                # Otherwise:
                else:
                    
                    # Skip over some exceptions
                    if (not (splitString[0].startswith("Actuator Type") or
                             splitString[0].startswith("BACnet Command Priority Array") or
                             splitString[0].startswith("None"))):
                             
                        # Make a new list to append the enumeration to
                        if (memEntry[2]):
                            memEntry = (memEntry[0], memEntry[1], False)
                            dictToAppend[memEntry[0]] = {}
                            dictToAppend[memEntry[0]][memEntry[1]] = []
                        toAppend = splitString[0].split('-')
                        
                        # If the format is really bad: exit
                        if (len(toAppend) != 2):
                            print("AHHHHHHHH NNNNNOOOOOOO!", toAppend[0], index)
                            exit(2)
                            
                        # Append enumeration
                        dictToAppend[memEntry[0]][memEntry[1]].append(toAppend[1].strip())
                    
                    # More Exception Stuff
                    if (splitString[0].startswith("BACnet Command Priority Array")):
                        index += 1
                index += 1
                
        # We aren't starting a new point, so ignore this line
        else:
            index += 1
    
    # Write the dictionary to a Json File
    with open(sys.argv[2], 'w') as jsonFile:
        json.dump(baseJsonDict, jsonFile)
        
    print("Done!")

if (__name__ == "__main__"):
    main()