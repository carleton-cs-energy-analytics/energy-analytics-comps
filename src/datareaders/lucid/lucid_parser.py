from datetime import datetime
import pandas as pd
import math
from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.data_object_holders import Point, PointType, PointValue


class LucidParser:
    """ A class for parsing the Lucid CSVs.
        I don't see this being used once we get this live,
        but for now it's what we are using. """

    def __init__(self):
        self.data = None  # Pandas DataFrame for storing CSV
        self.point_identities = None
        self.point_values = None

    def read_csv(self, file_name):
        self.data = pd.read_csv(file_name, dtype=object)

    def create_point_identities(self):
        """
        Function to create the point names for the Points database.
        Iterates through the column headers row 4 of Lucid CSV to parse out names with units.

        :return: None, sets the class variable to the list of new points.
        """
        point_identities = [] # This will be a list of each of the column headers as a Point object.

        point_names = list(self.data.iloc[3].copy())  # Get row that includes all point name data.
        for i in range(1, len(point_names)):
            # Get the name, the building name (sometimes the same thing) and the units information
            name, building_name, description = point_names[i].split(" - ")

            name = building_name + " - " + description.split("(")[0]

            # Clean up the unit information
            units = description.split(" ")[-1]
            units = units.replace("(", "")
            units = units.replace(")", "")

            # Create PointType class for Lucid Data Column
            point_type = PointType(name=name, return_type="float", units=units, factor=5)

            # Create Point Object from this column header information.
            new_point = Point(name=name, room_name=None, building_name=building_name,
                             source_enum_value=Sources.LUCID, point_type=point_type,
                             description=description)

            point_identities.append(new_point)

        self.point_identities = point_identities

    def create_point_values(self):
        """
        Function to create the point values for the PointValues database.
        Iterates through rows 5 - len(csv) to match timestamp with point value and name.

        :return: None, sets class variable to list of new timestamp, point, value tuples.
        """
        point_values = []

        num_row, num_col = self.data.shape
        for i in range(4, num_row):  # Iterate through every row after column headers

            cur_point_iden_index = 0  # Keep track of which column we are in.
            cur_row = list(self.data.iloc[i].copy())  # Copy the row so pandas doesn't overwrite the data somehow
            cur_timestamp = datetime.strptime(cur_row[0], "%m/%d/%y %H:%M")  # Get timestamp from column 0 of dataframe.

            for j in range(1, len(cur_row)):
                cur_point_identity = self.point_identities[cur_point_iden_index]  # Get point class for column we are in
                cur_point_value = cur_row[j]

                cur_point_value = float(cur_point_value)
                if math.isnan(cur_point_value):
                    cur_point_value = -2
                if cur_point_value > 0:
                    # Round cur_point_value to 5 decimal places.
                    cur_point_value = round(cur_point_value, 5)
                    # Multiply cur_point_value by 100000 to get as long int
                    cur_point_value *= 100000

                cur_point_value = int(cur_point_value)

                new_point_value = PointValue(cur_timestamp, cur_point_identity, cur_point_value)
                point_values.append(new_point_value)
                cur_point_iden_index += 1  # move to the next column.

        self.point_values = point_values


def main():
    file_name = get_data_resource("csv_files/Lucid_Data_10-16-17_to_10-16-17.csv")
    parser = LucidParser()
    parser.read_csv(file_name)
    parser.create_point_identities()
    parser.create_point_values()
    print("Finished!")


if __name__ == '__main__':
    main()
