import sys
import os

def main():
    files = next(os.walk("."))[2]
    for file in files:
        if (file.endswith("json")):
            os.system("python3 randoTest.py " + file)	    
    
if (__name__ == "__main__"):
	main()