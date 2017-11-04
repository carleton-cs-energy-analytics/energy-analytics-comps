from test.context import *
import unittest
import shutil

from src import read_csv

class TestReadCSV(unittest.TestCase):
    """Class for testing read_csv.py"""
    def setUp(self):
        self.PATH = sys.path[0]
        if os.path.isdir(self.PATH + "/../data/better_csv_files"):
            shutil.rmtree(self.PATH + "/../data/better_csv_files/")

    def tearDown(self):
        shutil.rmtree(self.PATH + "/../data/better_csv_files/")

    def test_transform_file(self):
        csv_path = self.PATH + "/../data/csv_files/"
        file_name = "HULINGS.AUDIT.TRENDRPT1_171016.csv"
        better_file_path = self.PATH + "/../data/better_csv_files/" + file_name

        read_csv.transform_file(csv_path+file_name)

        with open(better_file_path, "r") as new_csv:
            readlines = new_csv.readlines()

        self.assertTrue("Point" not in " ".join(readlines))

    def test_transform_all_files_make_better_csv_files(self):
        read_csv.transform_all_files()
        self.assertTrue(os.path.isdir(self.PATH + "/../data/better_csv_files"))

    def test_transform_all_files_all_transformations_appear(self):
        pre_transform = []
        for file in os.listdir(self.PATH + "/../data/csv_files/"):
            if file.endswith(".csv"):
                pre_transform.append(file)

        read_csv.transform_all_files()

        for file in os.listdir(self.PATH + "/../data/better_csv_files/"):
            if file.endswith(".csv"):
                self.assertIn(file, pre_transform)

if __name__ == "__main__":
    unittest.main()
