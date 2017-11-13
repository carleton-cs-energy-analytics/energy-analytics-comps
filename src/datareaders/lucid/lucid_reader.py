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
        self.file_path = get_data_resource("csv_files/" + file_name)
        self.source = source  # Use the enumeration for Lucid
        self.db_connection = DatabaseConnection()  # Start up connection to DB
        self.lucid_parser = LucidParser()  # initialize parser class for looking at CSVs
        self.lucid_parser.read_csv(self.file_path)  # Load CSV
        self.lucid_parser.create_point_identities()  # Create values to insert into Points Table
        self.lucid_parser.create_point_values()  # Create values to insert into PointValue Table


    def add_to_db(self):
        """
        Adds the points and point values from the loaded CSV file into the database.

        :return: None
        """

        successfully_inserted = []
        unsuccessfully_inserted = []
        for point in self.lucid_parser.point_identities:
            try:
                self.db_connection.add_unique_point(point)
                successfully_inserted.append("Inserted point " + point.name)
            except:
                unsuccessfully_inserted.append("Couldn't insert point: " + point.name)

        for item in successfully_inserted:
            print(item)
        for item in unsuccessfully_inserted:
            print(item)

        print("Was able to successfully insert {} points.".format(len(successfully_inserted)))
        print("Was NOT able to successfully insert {} points.".format(len(unsuccessfully_inserted)))


    def _add_building(self):
        '''
        Add unique building -- only adds if building not already in DB
        :return: None
        '''
        self.db_connection.add_unique_building(self.building_name)

