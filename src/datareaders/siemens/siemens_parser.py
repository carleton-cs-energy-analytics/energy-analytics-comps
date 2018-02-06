"""
Converts an ugly csv into a better one.
"""
import csv
import sys
import os
import io
from src.datareaders.resources import get_data_resource

def transform_csv(input_stream):
    """
    Takes in dataList, which represents the original CSV, and writes a new
    CSV file that has mapped all the point with their name.
    """
    # Find the first empty row and create a dictionary to map the points to their names:
    point_index = 1
    point_name_list = []
    reader = csv.reader(input_stream)
    data_list = list(reader)
    output_stream = io.StringIO()

    writer = csv.writer(output_stream)
    while "Point_" in data_list[point_index][0]:
        point_name_list.append(data_list[point_index][1])
        point_index += 1

    
    # Construct and write the first line
    first_line = ["Date","Time"]
    for name in point_name_list:
        first_line.append(name)

    writer.writerow(first_line)
    # Write the rest of the lines:
    for i in range(point_index + 5, len(data_list), 1):
        try:
            if '*******' in data_list[i][0]: # End of report
                break
            writer.writerow(data_list[i])
        except IndexError:
            #end of file, can just continue
            break
    return output_stream

def transform_all_files(directory_path = None):
    """
    Loops over every .csv file and calls transform_file function on it
    :return: None (Output better files in data/better_csv_files)
    """
    if not directory_path:
        directory_path = get_data_resource("csv_files")

    for file in os.listdir(directory_path):
        if file.endswith(".csv"):
            transform_file(get_data_resource("csv_files/"+file))

def transform_file(file_path):
    """
    Transforms an individual file
    :param file: file name
    :return: output stream
    """

    with open(file_path, 'r') as input_stream:
        output_stream = transform_csv(input_stream)
        output_stream.seek(0)
        return output_stream

def transform_string(input_string):
    input_stream = io.StringIO(input_string)
    input_stream.seek(0)
    output_stream = transform_csv(input_stream)
    output_stream.seek(0)
    return output_stream

def main():
    """
    Run `python3 -m src.datareaders.siemens.siemens_parser transform <file_name> to transform a CSV
    If no commandline arguments --> Transforms all .csv files in data/csv_files/
    :return: None
    """
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
