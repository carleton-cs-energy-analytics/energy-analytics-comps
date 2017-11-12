from datetime import datetime
import pandas as pd
from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.data_object_holders import Point, PointValue


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
        point_identities = []

        point_names = list(self.data.iloc[3].copy())
        for i in range(1, len(point_names)):
            name, building_name, description = point_names[i].split(" - ")

            name = building_name + " - " + description.split("(")[0]
            newPoint = Point(name=name, room_name=None, building_name=building_name,
                             source_enum_value=Sources.LUCID, point_type=None,
                             description=description)
            point_identities.append(newPoint)

        self.point_identities = point_identities

    def create_point_values(self):
        """
        Function to create the point values for the PointValues database.
        Iterates through rows 5 - len(csv) to match timestamp with point value and name.

        :return: None, sets class variable to list of new timestamp, point, value tuples.
        """
        point_values = []

        num_row, num_col = self.data.shape
        for i in range(4, num_row):
            cur_point_iden_index = 0
            cur_row = list(self.data.iloc[i].copy())
            cur_timestamp = datetime.strptime(cur_row[0], "%m/%d/%y %H:%M")
            for j in range(1, len(cur_row)):
                cur_point_identity = self.point_identities[cur_point_iden_index]
                newPointValue = PointValue(cur_timestamp, cur_point_identity, cur_row[j])
                point_values.append(newPointValue)
                cur_point_iden_index += 1

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
