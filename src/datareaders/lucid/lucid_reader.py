from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.lucid.lucid_parser import LucidParser
from src.datareaders.data_object_holders import Point, PointType
from json import load as json_load


class LucidReader:
    """TODO: Write docs for function. Since I'm not sure what form this is going to
       take, we'll come back to this..."""

    def __init__(self, input_stream, source):
        self.source = source  # Use the enumeration for Lucid
        self.db_connection = DatabaseConnection()  # Start up connection to DB
        self.lucid_parser = LucidParser()  # initialize parser class for looking at CSVs
        self.lucid_parser.read_csv(input_stream)  # Load CSV
        self.lucid_parser.create_point_identities()  # Create values to insert into Points Table
        self.lucid_parser.create_point_values()  # Create values to insert into PointValue Table

    def add_to_db(self):
        """
        Adds the points and point values from the loaded CSV file into the database.

        :return: None
        """

        self.add_points()
        self.add_point_values()

    def add_points(self):
        """
        Adds the points to the points table.

        :return: None
        """

        successfully_inserted = []
        unsuccessfully_inserted = []
        for point in self.lucid_parser.point_identities:
            try:
                self.db_connection.add_unique_building(point.building)
                self.db_connection.add_unique_room(point.room, point.building)
                self.db_connection.add_point_type(point.point_type)
                self.db_connection.add_unique_point(point)
                successfully_inserted.append("Inserted point " + point.name)
            except KeyError as e:
                print("Error: " + e)
                unsuccessfully_inserted.append("Couldn't insert point: " + point.name)

        for item in successfully_inserted:
            print(item)
        for item in unsuccessfully_inserted:
            print(item)

        print("Was able to successfully insert {} points.".format(len(successfully_inserted)))
        print("Was NOT able to successfully insert {} points.".format(len(unsuccessfully_inserted)))

    def add_point_values(self):
        """
        Adds the point values to the point values table.
        :return:
        """
        for point_value in self.lucid_parser.point_values:
            try:
                self.db_connection.add_unique_point_value(timestamp=point_value.timestamp, point=point_value.point,
                                                   value=point_value.value)
            except KeyError as e:
                print("Couldn't insert point!")
                print("Error: " + e)
        print("Finished trying to insert all point values!")


def main(input_stream):
    """
    Initialize lucid_parser, then put data into correct tables in DB.
    :return: None
    """
    lucid_reader = LucidReader(input_stream, source=Sources.LUCID)
    lucid_reader.add_to_db()
    lucid_reader.db_connection.close_connection()


if __name__ == '__main__':
    if not sys.stdin.isatty():
        # we have a stdin so get our input stream from that
        main(sys.stdin.read())
    else:
        path = get_data_resource("csv_files/Lucid_Data_10-16-17_to_10-16-17.csv")
        with open(path, 'r') as input_stream:
            main(input_stream)
