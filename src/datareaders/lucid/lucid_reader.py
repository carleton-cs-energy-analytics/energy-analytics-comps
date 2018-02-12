from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.lucid.lucid_parser import LucidParser
from src.datareaders.data_object_holders import Point, PointType
from json import load as json_load
import sys


class LucidReader:
    """TODO: Write docs for function. Since I'm not sure what form this is going to
       take, we'll come back to this..."""

    def __init__(self, input_stream, source):
        self.source = source  # Use the enumeration for Lucid
        self.db_connection = DatabaseConnection()  # Start up connection to DB
        self.lucid_parser = LucidParser()  # initialize parser class for looking at CSVs
        self.lucid_parser.read_csv(input_stream)  # Load CSV
        print("Creating Points")
        self.lucid_parser.add_points()  # Create values to insert into Points Table
        print("Creating Values")
        self.lucid_parser.add_point_values()  # Create values to insert into PointValue Table


def main(input_stream):
    """
    Initialize lucid_parser, then put data into correct tables in DB.
    :return: None
    """
    lucid_reader = LucidReader(input_stream, source=Sources.LUCID)
    lucid_reader.db_connection.close_connection()


if __name__ == '__main__':
    if not sys.stdin.isatty():
        # we have a stdin so get our input stream from that
        main(sys.stdin.read())
    else:
        file_name = "DormData2013-18.csv"
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
        path = get_data_resource("csv_files/"+file_name)
        with open(path, 'r') as input_stream:
            main(input_stream)
