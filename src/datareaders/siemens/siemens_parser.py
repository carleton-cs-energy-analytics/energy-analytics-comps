"""
Converts an ugly csv into a better one.
"""
import csv
import sys
import os
from src.datareaders.resources import get_data_resource

def transform_csv_from_bad_format_to_better_format(data_list, new_csv_name):
    """
    Takes in dataList, which represents the original CSV, and writes a new
    CSV file that has mapped all the point with their name.
    """
    # Find the first empty row and create a dictionary to map the points to their names:
    point_index = 1
    point_name_list = []
    while "Point_" in data_list[point_index][0]:
        point_name_list.append(data_list[point_index][1])
        point_index += 1

    # Write the new data to a CSV:
    with open(new_csv_name, 'w') as f:
        writer = csv.writer(f)
        
        # Construct and write the first line
        first_line = ["Date","Time"]
        for name in point_name_list:
            first_line.append(name)

        writer.writerow(first_line)

        # Write the rest of the lines:
        for i in range(point_index + 5, len(data_list), 1):
            writer.writerow(data_list[i])

def transform_all_files(directory_path = None):
    '''
    Loops over every .csv file and calls transform_file function on it
    :return: None (Output better files in data/better_csv_files)
    '''
    if not directory_path:
        directory_path = get_data_resource("csv_files")

    for file in os.listdir(directory_path):
        if file.endswith(".csv"):
            transform_file(get_data_resource("csv_files/"+file))

def transform_file(file_path, better_dir_path = None):
    '''
    Transforms an individual file
    :param file: file name
    :return: None (Output is better file format in data/better_csv_files)
    '''
    if not better_dir_path:
        better_dir_path = get_data_resource("better_csv_files")
    # Create directory for transforming csvs into better format
    if not os.path.isdir(better_dir_path):
        os.makedirs(better_dir_path)

    better_file_name = better_dir_path + "/" + file_path.split("/")[-1]
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data_list = list(reader)
    transform_csv_from_bad_format_to_better_format(data_list, better_file_name)

def main():
    '''
    Run `python3 -m src.datareaders.siemens.siemens_parser transform <file_name> to transform a CSV
    If no commandline arguments --> Transforms all .csv files in data/csv_files/
    :return: None
    '''
    if len(sys.argv) > 1:
        # CASE: transform the CSV from the bad input to the better one
        if sys.argv[1] == "transform":
            directory_path = get_data_resource('csv_files')
            file = sys.argv[2]
            transform_file(directory_path, file)

    # CASE: transforms every .csv file in csv_files to a better format
    else:
        transform_all_files()

if __name__ == "__main__":
    main()
