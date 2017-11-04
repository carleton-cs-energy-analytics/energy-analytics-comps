import unittest
import shutil
import os, sys
from src.datareaders.siemens import transform_csv
from src.datareaders.resources import get_data_resource


class TestTransformCSV(unittest.TestCase):
    """Class for testing read_csv.py"""
    def setUp(self):
        if os.path.isdir(get_data_resource("better_csv_files")):
            shutil.rmtree(get_data_resource("better_csv_files"))

    def tearDown(self):
        shutil.rmtree(get_data_resource("better_csv_files"))

    def test_transform_file(self):
        file_name = "HULINGS.AUDIT.TRENDRPT1_171016.csv"
        better_file_path = get_data_resource("better_csv_files") + file_name

        transform_csv.transform_file(get_data_resource("csv_files/"+file_name))

        with open(better_file_path, "r") as new_csv:
            readlines = new_csv.readlines()

        self.assertTrue("Point" not in " ".join(readlines))

    def test_transform_all_files_make_better_csv_files(self):
        transform_csv.transform_all_files()
        self.assertTrue(os.path.isdir(get_data_resource("better_csv_files")))

    def test_transform_all_files_all_transformations_appear(self):
        pre_transform = []
        for file in os.listdir(get_data_resource("csv_files")):
            if file.endswith(".csv"):
                pre_transform.append(file)

        transform_csv.transform_all_files()

        for file in os.listdir(get_data_resource("better_csv_files")):
            if file.endswith(".csv"):
                self.assertIn(file, pre_transform)

if __name__ == "__main__":
    unittest.main()
