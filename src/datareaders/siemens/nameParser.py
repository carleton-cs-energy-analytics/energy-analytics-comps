import json
import sys
from src.datareaders.resources import get_data_resource

# Call with: python3 nameParser <dictionary_file> <name of point>
# Where <dictionary_file> will almost always be ????? (Ask Carolyn)


def main():
    nameLookUpDictionary = {}
    with open(get_data_resource("csv_descriptions/"+sys.argv[1]), 'r') as jsonFile:
        jsonDict = json.load(jsonFile)
        
    with open(get_data_resource("csv_descriptions/"+sys.argv[2]), 'r') as pointListFile:
        pointList = json.load(pointListFile)
    
    counter = 0
    parsed = 0
    unparseable = 0
    for (k,v) in pointList.items():
        counter += 1
        tagsSet = decodeName(k, jsonDict)
        if (tagsSet != None):
            if (tagsSet == "Not quite"):
                unparseable += 1
            else :
                parsed += 1
#                print (k, "\n" +  stringHumanReadable(tagsSet, jsonDict))
#                print (k, tagsSet)
                print (k, tagName(k, jsonDict))

    print (parsed, counter - unparseable, counter, float(parsed * 100) / float(counter - unparseable), float(parsed * 100) / float(counter))

def stringHumanReadable(tags, dictionary):
    string = ""
    for tag in tags:
        string += " -> " + dictionary[tag[0]]["type"] + ": " + dictionary[tag[0]]["descriptor"]
        if (len(tag) > 1):
            string += " (indexed by: " + tag[1] + ")"
        string += "\n"
    return string
        
        
## Build in exceptions for:
#   > Building names with room number accocieted
#   > Electric/Water meter data (today v. month v. yest) 
#   > CH: [E]AST, MH: [W]EST
#   > SPTA -> Actual
#        FCU -> Fan cooling unit


#  Building report: top 5 buildings (or so)

def tagName(name, dictionary):
    tagSet = decodeName(name, dictionary)
    if ((tagSet == None) or (tagSet == "Not quite")):
        return None
    tagDict = {}
    for tag in tagSet:
        if (tag[0] == 'ROOM'):
            if (len(tag) > 1):
                tagDict['ROOM'] = tag[1:2]
        else:
            tagDict[dictionary[tag[0]]["type"]] = tag
    return tagDict


def decodeName(name, dictionary):
    revDict = createRevDict(dictionary)
    nameSubstrings = preProcessName(name)
    if (nameSubstrings != None):
         testIndex = 0
         tagList = []
         while (testIndex < len(nameSubstrings)):
             substring = getTokenString(nameSubstrings[testIndex])
             if (substring not in revDict):
                 return None
             else:
                 tag = ""
                 for tagPossible in revDict[substring]:
                     tag = tagPossible
                 addedTag = False
                 if (dictionary[tag]["indexed"] == "True"):
                     if (testIndex + 1 < len(nameSubstrings)):
                         if (isNumberToken(nameSubstrings[testIndex + 1])):
                             testIndex += 1
                             tagList.append([tag, getTokenString(nameSubstrings[testIndex])])
                             addedTag = True
                 if (dictionary[tag]["type"] == "Building"):
                     if (testIndex + 1 < len(nameSubstrings)):
                         if ((name[1] == 'V') and ((name[0] == 'O') or (name[0] == 'B'))):
                             testIndex += 1
                             tagList.append([tag])
                             tagList.append(["VAV", getTokenString(nameSubstrings[testIndex])])
                             addedTag = True
#                         if (isNumberToken(nameSubstrings[testIndex + 1]) and not name.startswith('BIG')):
#                             testIndex += 1
#                             tagList.append([tag])
#                             tagList.append(["ROOM", getTokenString(nameSubstrings[testIndex])])
#                             addedTag = True
#                             print ("----> hello", name)
                 if ("toss" in dictionary[tag]):
                     for toToss in dictionary[tag]["toss"]:
                         toToss = 't' + toToss
                         if (toToss in nameSubstrings):
                             nameSubstrings.remove(toToss)
                 if ("parent" in dictionary[tag]):
                     validTag = False
                     for currTag in tagList:
                         if (currTag[0] == dictionary[tag]["parent"]):
                             validTag = True
                     if (not validTag):
                         return None
                 if (not addedTag):
                     tagList.append([tag])
             testIndex += 1
#         print (name, tagList)
         return tagList
    return "Not quite"

def createRevDict(dictionary):
    revDict = {}
    for (k,v) in dictionary.items():
        for subname in v["name"]:
            if (subname not in revDict):
                revDict[subname] = []
            revDict[subname].append(k)
    return revDict

# Splits the name into differnt sections.
# Splits on '.' ':' and '-' and on some numbers
def preProcessName(name):
    subString = []
    subString.append("")
    for ch in name:
        if (ch == '.' or ch == ':' or ch == '-'):
            subString.append("")
        else:
            subString[-1] += ch
    i = 0
    
    if (len(subString) == 1):
        return None
    
    while (i < len(subString)):
        coveredCase = False
        numberSplit = False
        ## Some Exceptions ##
        if (subString[i] == 'H2O'):
            subString[i] = 'tH2O'
            coveredCase = True
        if (subString[i] == 'RB02A'):
            subString[i] = 'tRM'
            subString.insert(i + 1, '#B02A')
            i += 1
            coveredCase = True
        if (subString[i] == 'FLH'):
            if ((len(subString) > i + 2) and ((subString[i + 1][0] == 'E') or (subString[i + 1][0] == 'W'))):
                subString[i] = 'tRM'
                subString[i + 1] = '#' + subString[i + 1][1:]
                subString[i + 2] = 'FLH.' + subString[i + 2]
                i += 1
                coveredCase = True

        
        # Splice Numbers off the back
        if (subString[i].startswith('R') or subString[i].startswith('RM')):
           spliceIndex = 2
           if (subString[i].startswith('R')):
               spliceIndex = 1
           if (subString[i][spliceIndex] in '0123456789G'):
               subString.insert(i + 1, '#' + subString[i][spliceIndex:])
               subString[i] = 't' + subString[i][:spliceIndex]
               i += 1
               coveredCase = True
               numberSplit = True
        
        # 'Regular' case.  Check to split off the index
        if (not coveredCase):
            subTag = ""
            j = 1
            while (j < len(subString[i])):
                if (subString[i][j] in '0123456789'):
                    subTag = subString[i][j:]
                    subString[i] = subString[i][:j]
                j += 1
            subString[i] = 't' + subString[i]
            if (subTag != ""):
                i += 1
                subTag = '#' + subTag
                subString.insert(i, subTag)
                numberSplit = True
        
        # Check for equipement trailing behind the index of the equipment
        if (numberSplit):
            subTag = ""
            j = 2
            while (j < len(subString[i])):
                if (subString[i][j] not in '0123456789ABCDEG'):
                    subTag = subString[i][j:]
                    subString[i] = subString[i][:j]
                j += 1
            if (subTag != ""):
                i += 1
                subTag = 't' + subTag
                subString.insert(i, subTag)
                numberSplit = True
        i += 1
  
    return subString
        
        
#==============================================================
#                  Parse out number sections
#==============================================================

def isNumberToken(token):
    return (token[0] == '#')

def getTokenString(token):
    return (token[1:])


if (__name__ == "__main__"):
    main()