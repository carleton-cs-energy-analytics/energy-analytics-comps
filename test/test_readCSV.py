import unittest
import csv

#TODO anyone know how to do this better than what it is now?
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from src import readCSV

class TestReadCSV(unittest.TestCase):

    def test_transfromCSVFromBadFormatToBetterFormat(self):
        fileName = "TestCSV.csv"
        betterFileName = "better" + fileName

        with open(fileName, 'r') as f:
            reader = csv.reader(f)
            dataList = list(reader)

        readCSV.transfromCSVFromBadFormatToBetterFormat(
            dataList=dataList, newCSVName=betterFileName)

        new_csv = open(betterFileName, "r")

        readlines = new_csv.readlines()
        self.assertTrue("Point" not in " ".join(readlines))
        new_csv.close()

if __name__ == "__main__":
    unittest.main()
