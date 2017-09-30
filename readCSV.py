import csv

def main():
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        dataList = list(reader)
    
    # dataList now is a 2x2 matix representing the CSV.
        
        
if __name__ == "__main__":
    main()