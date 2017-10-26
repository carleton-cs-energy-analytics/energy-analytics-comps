import unittest
import csv

#TODO anyone know how to do this better than what it is now?
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from src import readCSV

class TestReadCSV(unittest.TestCase):

    def test_transfromCSVFromBadFormatToBetterFormat(self):
        fileName = "TestCSV.csv_files"
        betterFileName = "better" + fileName

        with open(fileName, 'r') as f:
            reader = csv.reader(f)
            dataList = list(reader)

        readCSV.transform_csv_from_bad_format_to_better_format(
            dataList=dataList, newCSVName=betterFileName)

        new_csv = open(betterFileName, "r")

        readlines = new_csv.readlines()
        self.assertTrue("Point" not in " ".join(readlines))
        new_csv.close()

if __name__ == "__main__":
    unittest.main()
