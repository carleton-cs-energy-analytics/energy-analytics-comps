import json
import sys

# Call with: python3 nameParser <dictionary_file> <name of point>
# Where <dictionary_file will almost always be ????? (Ask Carolyn)


def main():
    nameLookUpDictionary = {}
    with open(sys.argv[1], 'r') as jsonFile:
        jsonDict = json.load(jsonFile)
        
    with open(sys.argv[2], 'r') as pointListFile:
        pointList = json.load(pointListFile);
        
    for (k,v) in pointList:
        tagsSet = decodeName(k, jsonDict);
        
    


def decodeName(name, dictionary):
    nameSubstrings = preProcessName(name)
    if (nameSubstrings != None):
        
    
def preProcessName(name):
    if (len(name) == 6):
        return None
    else:
        subString = []
        subString.append("")
        for ch in name:
            if (ch == '.' or ch == ':' or ch == '-'):
                subString.append("")
            else:
                substring[-1] += ch
        for i in range(len(subString)):
            while (subString[i][-1] in '0123456789'):
                
        return subString


if (__name__ == "__main__"):
    main()