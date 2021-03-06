import unittest
import shutil
import os, sys
from src.datareaders.siemens import siemens_parser
from src.datareaders.resources import get_data_resource


class TestTransformCSV(unittest.TestCase):
    """Class for testing read_csv.py"""


    def test_transform_file(self):
        file_name = "HULINGS.AUDIT.TRENDRPT1_171016.csv"

        new_csv = siemens_parser.transform_file(get_data_resource("csv_files/" + file_name))

        readlines = new_csv.readlines()

        self.assertTrue("Point" not in " ".join(readlines))

    def test_transform_all_files_make_better_csv_files(self):
        results = siemens_parser.transform_all_files()
        self.assertTrue(len(results) > 0)

    def test_transform_all_files_all_transformations_appear(self):
        pre_transform = []
        for file in os.listdir(get_data_resource("csv_files")):
            if file.endswith(".csv"):
                pre_transform.append(file)

        results = siemens_parser.transform_all_files()
        self.assertTrue(len(results) == len(pre_transform))

if __name__ == "__main__":
    unittest.main()
