import unittest
import csv

#TODO anyone know how to do this better than what it is now?
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from src import readCSV

class TestReadCSV(unittest.TestCase):

    def setUp(self):
        self.PATH = "/Users/Carolyn/PycharmProjects/energy-analytics-comps/"

    def test_transfromCSVFromBadFormatToBetterFormat(self):
        fileName = "TestCSV.csv"
        betterFileName = "better" + fileName

        with open(self.PATH+fileName, 'r') as f:
            reader = csv.reader(f)
            dataList = list(reader)

        readCSV.transfromCSVFromBadFormatToBetterFormat(
            dataList=dataList, newCSVName=self.PATH+betterFileName)

        new_csv = open(self.PATH+betterFileName, "r")

        readlines = new_csv.readlines()
        self.assertTrue("Point" not in " ".join(readlines))
        new_csv.close()

if __name__ == "__main__":
    unittest.main()
