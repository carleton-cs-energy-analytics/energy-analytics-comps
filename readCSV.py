import csv
import sys
import pandas as pd

# Run "python3 readCSV.py transform <nameOfFile>"
#    to read in the CSV and transform it into a better format
# If no commandLine arguments are passed into it, then it passed the
#    CSV into pandas.
def main():
    if (len(sys.argv) > 1):
        # CASE: transform the CSV from the bad input to the better one
        if sys.argv[1] == "transform":
            fileName = sys.argv[2]
            betterFileName = "better" + fileName
            with open(fileName, 'r') as f:
                reader = csv.reader(f)
                dataList = list(reader)
            
            transfromCSVFromBadFormatToBetterFormat(dataList, betterFileName)
        else:
            fileName = sys.argv[1]
            get_dataframe_from_csv(fileName)

    # CASE: everything else we are trying to do.
    else:
        # No Sys args, just use test file
        get_dataframe_from_csv("betterTestCSV.csv") # Need to run transform first to get this file

# takes in dataList, which represents the original CSV, and writes a new
# CSV file that has mapped all the point with their name.
def transfromCSVFromBadFormatToBetterFormat(dataList, newCSVName):
    # Find the first empty row and create a dictionary to map the points to their names:
    split = 0
    pointToName = {}
    while (split < len(dataList) and dataList[split][0] != ""):
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

def get_dataframe_from_csv(fileName):
    df = pd.read_csv(fileName, dtype=object)

    # Potential example of finding cycling?
    previous_entry = None
    cycle_count = 0
    for entry in df._series['ACDIN.VAV026:HEAT.COOL']:
        if entry != previous_entry and previous_entry != None:
            cycle_count += 1
        previous_entry = entry
    print("{} cycles(?) in this example".format(cycle_count))

    for index, row in df.iterrows():
        # print(row)
        pass
        
if __name__ == "__main__":
    main()