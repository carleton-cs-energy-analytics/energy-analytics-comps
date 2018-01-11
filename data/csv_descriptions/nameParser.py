import json
import sys

def main():
    jsonObject = {}
    with open(sys.argv[1], 'r') as jsonFile:
        jsonObject = json.load(jsonFile)



















if (__name__ == "__main__"):
    main()