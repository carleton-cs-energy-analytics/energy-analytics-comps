"""
Converts an ugly csv into a better one.
"""

import csv
import sys
import pandas as pd


def transform_csv_from_bad_format_to_better_format(data_list, new_csv_name):
    """
    Takes in dataList, which represents the original CSV, and writes a new
    CSV file that has mapped all the point with their name.
    """
    # Find the first empty row and create a dictionary to map the points to their names:
    split = 0
    point_to_name = {}
    while split < len(data_list) and data_list[split][0] != "":
        point_to_name[(data_list[split][0])[:-1]] = data_list[split][1]
        split += 1
    
    # Write the new data to a CSV:
    with open(new_csv_name, 'w') as f:
        writer = csv.writer(f)
        
        # Construct and write the first line
        first_line = [data_list[split + 1][0], data_list[split + 1][1]]
        for j in range(2, len(data_list[split + 1]), 1):
            first_line.append(point_to_name[data_list[split + 1][j]])
        writer.writerow(first_line)
        
        # Write the rest of the lines:
        for i in range(split + 2, len(data_list), 1):
            writer.writerow(data_list[i])


def get_dataframe_from_csv(file_name):
    """Make csv_files into Pandas data frame"""
    df = pd.read_csv(file_name, dtype=object)

    # Potential example of finding cycling?
    previous_entry = None
    cycle_count = 0
    for entry in df._series['ACDIN.VAV026:HEAT.COOL']:
        if entry != previous_entry and previous_entry is not None:
            cycle_count += 1
        previous_entry = entry
    print("{} cycles(?) in this example".format(cycle_count))

    for index, row in df.iterrows():
        # print(row)
        pass


def main():
    """Run "python3 read_csv.py transform <nameOfFile>" to read in the CSV and transform it into a better format
    If no commandLine arguments are passed into it, then it passed the CSV into pandas."""
    if len(sys.argv) > 1:

        # CASE: transform the CSV from the bad input to the better one
        if sys.argv[1] == "transform":
            file_name = sys.argv[2]
            better_file_name = "better" + file_name
            with open(file_name, 'r') as f:
                reader = csv.reader(f)
                data_list = list(reader)
            transform_csv_from_bad_format_to_better_format(data_list, better_file_name)
        else:
            file_name = sys.argv[1]
            get_dataframe_from_csv(file_name)

    # CASE: everything else we are trying to do.
    else:
        # No Sys args, just use test file
        get_dataframe_from_csv("../data/csv_files/betterTestCSV.csv_files")  # Need to run transform first to get this file

        
if __name__ == "__main__":
    main()
