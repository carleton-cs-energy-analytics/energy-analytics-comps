from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.data_object_holders import Point, PointType, PointValue
from json import load as json_load
import pandas as pd
from datetime import datetime
import math


class LucidReader:
    # TODO: TEST THIS!!!!!

    def __init__(self, file_name, source):
        self.file_path = get_data_resource("csv_files/" + file_name)
        self.source = Sources.LUCID  # Use the enumeration for Lucid
        self.db_connection = DatabaseConnection()  # Start up connection to DB
        self.data = pd.read_csv(self.file_path, dtype=object)

    def add_to_db(self):
        """
        Adds the points and point values from the loaded CSV file into the database.

        :return: None
        """
        index_to_point = self.add_points()
        self.add_point_values(index_to_point)

    def add_points(self):
        """
        Adds the points to the points table.

        :return: None
        """

        successfully_inserted = []
        unsuccessfully_inserted = []
        index_to_point = {}

        point_names = list(self.data.iloc[3].copy())  # Get row that includes all point name data.
        for i in range(1, len(point_names)):

            # Get the name, the building name (sometimes the same thing) and the units information
            name, building_name, description = point_names[i].split(" - ")
            name = building_name + " - " + description.split("(")[0]
            if "Old Meter" in description:  # We need to differentiate between old meters and new ones.
                name = name + "(Old Meter)"

            # Clean up the unit information
            units = description.split(" ")[-1]
            units = units.replace("(", "")
            units = units.replace(")", "")

            try:
                building_id = self.db_connection.add_unique_building(building_name)
                room = "{}_Dummy_Room".format(building_name)
                room_id = self.db_connection.add_unique_room(room, building_id)

                # Create PointType class for Lucid Data Column
                point_type = PointType(name=name, return_type="float", units=units, factor=5)
                point_type_id = self.db_connection.add_unique_point_type(point_type)

                # Create Point Object from this column header information.
                point = Point(name=name, room_id=room_id, building_id=building_id,
                              source_enum_value=Sources.LUCID, point_type_id=point_type_id,
                              description=description)
                point_id = self.db_connection.add_unique_point(point)
                point.id = point_id
                index_to_point[i] = point
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

        return index_to_point

    def add_point_values(self, index_to_point):
        """
        Adds the point values to the point values table.
        :return:
        """
        num_row, num_col = self.data.shape
        for i in range(4, num_row):  # Iterate through every row after column headers
            if i not in index_to_point:
                continue # didn't insert this point into the db
            cur_row = list(
                self.data.iloc[i].copy())  # Copy the row so pandas doesn't overwrite the data somehow
            cur_timestamp = datetime.strptime(cur_row[0],
                                              "%m/%d/%y %H:%M")  # Get timestamp from column 0 of dataframe.

            for j in range(1, len(cur_row)):
                try:
                    cur_point = index_to_point[j]  # Get point class for column we are in

                    cur_point_value = cur_row[j]

                    cur_point_value = float(cur_point_value)
                    if math.isnan(cur_point_value):
                        cur_point_value = None
                    if cur_point_value > 0:
                        # Round cur_point_value to 5 decimal places.
                        cur_point_value = round(cur_point_value, 5)
                        # Multiply cur_point_value by 100000 to get as long int
                        cur_point_value *= 100000

                    cur_point_value = int(cur_point_value)

                    self.db_connection.add_unique_point_value(timestamp=cur_timestamp, point_id=cur_point.id,
                                                                value=cur_point_value)
                except ValueError as e:
                    print("Error: " + e)
                    continue
        print("Finished trying to insert all point values!")


def main():
    """
    Initialize lucid_parser, then put data into correct tables in DB.
    :return: None
    """
    lucid_reader = LucidReader(file_name="/Lucid_Data_10-16-17_to_10-16-17.csv", source=Sources.LUCID)
    lucid_reader.add_to_db()
    lucid_reader.db_connection.close_connection()


if __name__ == '__main__':
    main()
