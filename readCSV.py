import csv
import sys

def main():
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        dataList = list(reader)
    
    # dataList now is a 2x2 matix representing the CSV.
    
    for row in dataList:
       line = ""
       for cell in row:
          line = line + cell + ", "
       print (line)

def transfromCSVFromBadFormatToBetterFormat(dataList, newCSVName):
    # Find the first empty row and create a dictionary to map the points to their names:
    split = 0
    pointToName = {}
    while (dataList[split][0] != ""):
        pointToName[dataList[split][0]] = dataList[split][1]
        split += 1
    
    
    
        
if __name__ == "__main__":
    main()