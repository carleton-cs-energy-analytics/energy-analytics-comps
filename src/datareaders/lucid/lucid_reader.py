from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.lucid.lucid_parser import LucidParser
from src.datareaders.data_object_holders import Point, PointType
from json import load as json_load



class LucidReader:
    """TODO: Write docs for function. Since I'm not sure what form this is going to
       take, we'll come back to this..."""

    def __init__(self, file_name, source):
        self.file_path = get_data_resource("csv_files/" +file_name)
        self.building_name = None #TODO: Decide how to set building data
        self.source = source # Use the enumeration for Lucid
        self.db_connection = DatabaseConnection() # Start up connection to DB
        self.lucid_parser = LucidParser() # initialize parser class for looking at CSVs
        self.lucid_parser.read_csv(self.file_path)


    def add_to_db(self):

        pass


