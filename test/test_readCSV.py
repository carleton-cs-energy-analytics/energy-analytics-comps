import csv
import os
import sys
import unittest

# TODO anyone know how to do this better than what it is now?
sys.path.insert(0, os.path.abspath('..'))
from src import read_csv


class TestReadCSV(unittest.TestCase):

    def test_transform_csv_from_bad_format_to_better_format(self):

        csv_path = "../data/csv_files/"
        file_name = csv_path + "TestCSV.csv"
        better_file_name = csv_path + "betterTestCSV.csv"

        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            data_list = list(reader)

        read_csv.transform_csv_from_bad_format_to_better_format(
            data_list=data_list,
            new_csv_name=better_file_name
        )

        new_csv = open(better_file_name, "r")

        readlines = new_csv.readlines()
        self.assertTrue("Point" not in " ".join(readlines))
        new_csv.close()


if __name__ == "__main__":
    unittest.main()
