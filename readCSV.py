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
        
        
if __name__ == "__main__":
    main()