import sys
import csv
import json

def main():
    with open(sys.argv[1], 'rU') as csvFile:
        fileReader = csv.reader(csvFile)
        fileContents = list(fileReader)
    
    newList = [line[0].strip() for line in fileContents if len(line) > 0]
    
    baseJsonDict = {}
    index = 0;
    while (index < len(newList)):
        if (newList[index].startswith("Point System Name")):
            dictToAppend = {}
            memEntry = None;
            baseJsonDict[newList[index].split(':', 1)[1].strip()] = dictToAppend
            index += 1
            while (not ((newList[index] == '') or (newList[index].startswith("******")))):
                splitString = newList[index].split(':', 1)
                if (len(splitString) != 1):
                    dictToAppend[splitString[0]] = splitString[1].strip()
                    memEntry = (splitString[0], dictToAppend[splitString[0]], True);
                else:
                    if (not (splitString[0].startswith("Actuator Type") or
                             splitString[0].startswith("BACnet Command Priority Array") or
                             splitString[0].startswith("None"))):
	                    if (memEntry[2]):
	                        memEntry = (memEntry[0], memEntry[1], False)
	                        dictToAppend[memEntry[0]] = {}
	                        dictToAppend[memEntry[0]][memEntry[1]] = []
	                    toAppend = splitString[0].split('-')
	                    if (len(toAppend) != 2):
	                        print("AHHHHHHHH NNNNNOOOOOOO!", toAppend[0], index)
	                        exit(2)
	                    dictToAppend[memEntry[0]][memEntry[1]].append(toAppend[1].strip())
                index += 1
        else:
            index += 1
    
    with open(sys.argv[2], 'w') as jsonFile:
        json.dump(baseJsonDict, jsonFile)
        
    print("Done!")

if (__name__ == "__main__"):
	main()