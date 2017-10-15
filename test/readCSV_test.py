from nose.tools import assert_equals
import csv
import sys
import os
sys.path.insert(0, '~/PycharmProjects/energy-analytics-comps')

from src import readCSV
PATH = "/Users/Carolyn/PycharmProjects/energy-analytics-comps/"
def test_transfromCSVFromBadFormatToBetterFormat():
    fileName = "TestCSV.csv"
    betterFileName = "better" + fileName

    with open(PATH+fileName, 'r') as f:
        reader = csv.reader(f)
        dataList = list(reader)

    readCSV.transfromCSVFromBadFormatToBetterFormat(
        dataList=dataList, newCSVName=PATH+betterFileName)

    new_csv = open(PATH+betterFileName, "r")

    readlines = new_csv.readlines()
    assert_equals("Point" not in " ".join(readlines), True)
