import json
import sys

def terminate(code):
    print("OH NOES!!!!", code, sys.argv[1])
    exit();

class Item():
    def __init__(self, entry):
        if ("Text Table" in entry):
            self.tt = True
            self.table = entry["Text Table"]
        else:
            self.tt = False
            self.ar = entry["Analog Representation"]
            self.eu = entry["Engineering Units"]
    
    def testEq(self, other)s:
#        return (self.tt == other.tt)
        if (self.tt and other.tt):
            key1 = list(self.table.keys())[0]
            key2 = list(other.table.keys())[0]
            if (key1 == key2):
                if (len(self.table[key1]) == len(other.table[key2])):
                    for i in range(len(self.table[key1])):
                        if (self.table[key1][i] != other.table[key2][i]):
                            return False
                    return True     
                else:
                    return False
            else:
                return False
        elif ((not self.tt) and (not other.tt)):
            return self.ar == other.ar
#            return ((self.ar == other.ar) and (self.eu == other.eu))
        else:
            return False
    

def main():
    print ("Start: ", sys.argv[1])
    jsonObject = {}
    with open(sys.argv[1], 'r') as jsonFile:
        jsonObject = json.load(jsonFile)
        
    
    randoDict = {}
    count1 = 0;
    count2 = 0;
    for k,v in jsonObject.items():
        count1 += 1
        endStr = k.split(".")
        toTerm = 0
        for part in endStr:
            if (isRm(part)):
                toTerm += 1
        if (toTerm != 1):
            count2 += 1
    
    print(count1 - count2, " ", count1)
#         if ("Analog Representation" in v):
#             ent = v["Analog Representation"]
#             if (not ((ent.lower() == "float") or (ent.lower() == "integer"))):
#                 terminate(k)
                 
#        endStr = k.split(".", 2)[-1]
#        if (endStr in randoDict):
#            if (not randoDict[endStr].testEq(Item(v))):
#                terminate(k);
#        else:
#            randoDict[endStr] = Item(v)
    
#        tt = "Text Table" in v
#        ar = "Analog Representation" in v
#        eu = "Engineering Units" in v
#        if ((tt and (ar and eu))):
#            termiante(k);   
    print ("Done!")


def isRm(a):
   for ch in a:
       if ((not isDig(ch)) and (ch != "R") and (ch != "M")):
           return False
   for ch in "0123456789":
       for cha in a:
           if (ch == cha):
               return True
   return False

def isDig(a):
    for ch in "0123456789":
        if (ch == a):
            return True
    return False
        
    
if (__name__ == "__main__"):
    main()