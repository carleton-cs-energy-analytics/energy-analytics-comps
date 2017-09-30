import csv
import sys

def main():
    fileName = sys.argv[1]
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        dataList = list(reader)
    
    # dataList now is a 2x2 matix representing the CSV.
    transfromCSVFromBadFormatToBetterFormat(dataList, "better" + fileName + ".csv");

# takes in dataList, which represents the original CSV, and writes a new
# CSV file that has mapped all the point with their name.
def transfromCSVFromBadFormatToBetterFormat(dataList, newCSVName):
    # Find the first empty row and create a dictionary to map the points to their names:
    split = 0
    pointToName = {}
    while (dataList[split][0] != ""):
        pointToName[(dataList[split][0])[:-1]] = dataList[split][1]
        split += 1
    
    # Write the new data to a CSV:
    with open(newCSVName, 'w') as f:
        writer = csv.writer(f)
        
        # Construct and write the firstline:
        firstLine = [dataList[split + 1][0], dataList[split + 1][1]]
        for j in range(2, len(dataList[split + 1]), 1):
            firstLine.append(pointToName[dataList[split + 1][j]])
        writer.writerow(firstLine)
        
        # Write the rest of the lines:
        for i in range(split + 2, len(dataList), 1):
            writer.writerow(dataList[i])
        
if __name__ == "__main__":
    main()