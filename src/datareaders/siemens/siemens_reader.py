"""
Reads a given csv file and adds all information to the database
"""
from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.data_object_holders import Point, PointType
from src.datareaders.siemens.siemens_parser import transform_file, transform_string
from json import load as json_load
import sys
import pandas as pd


class SiemensReader:
    def __init__(self, input_stream, building, source):
        self.building_name = building
        self.source = source
        self.db_connection = DatabaseConnection()
        self.siemens_data = pd.read_csv(input_stream, dtype=object)
        json_file = open(get_data_resource("csv_descriptions/testPointJson_{}.json".format(building)), "r")
        self.json_dict = json_load(json_file)
        self.points = {}

    def add_to_db(self):
        """
        Adds building, rooms, point types, and point to the database
        :return: None
        """
        self._add_building()
        finish_lst = []
        cant_finish_lst = []
        for point_name in self.siemens_data.columns[2:]:
            try:
                room_name = self._add_room(point_name)
                point_type = self._get_point_type(point_name)
                description = self.json_dict[point_name]["Descriptor"]

                point = Point(point_name, room_name, self.building_name, self.source, point_type, description)
                point_id = self.db_connection.add_unique_point(point)
                point.id = point_id

                self.points[point_name] = point
                finish_lst.append("Finished for point "+point_name)
            except KeyError:
                cant_finish_lst.append("Don't know type of "+point_name)

        for item in finish_lst:
            print(item)

        for item in cant_finish_lst:
            print(item)

        print("Was able to successfully add {} points".format(len(finish_lst)))
        print("Was NOT able to add {} points".format(len(cant_finish_lst)))

        self._add_point_values()

    def _add_building(self):
        """
        Add unique building -- only adds if building not already in DB
        :return: None
        """
        self.db_connection.add_unique_building(self.building_name)

    def _add_room(self, point_name):
        """
        Add unique room -- only adds if room not already in DB
        :param point_name: String of point name --> not used but should be if we want real rooms!
        :return: Room name (str)
        """
        room = "{}_Dummy_Room".format(self.building_name)
        point_name_split = point_name.split(".")
        if len(point_name_split) > 1:
            possible_room = point_name_split[1]
            if len(possible_room) > 1 and possible_room[0] == 'R' and possible_room[1:].isdigit():
                room = possible_room[1:]

        self.db_connection.add_unique_room(room, self.building_name)
        return room

    def _read_hardcoded_types(self):
        """
        Reads name - type pairs from a given file
        """
        hardcoded_types = {}
        return hardcoded_types

    def _get_point_type(self, point_name):
        """
        Returns the point type for the given name
        If from the hardcoded types, name will be reasonable
        If new type, name will be a concatenation of return_type and units/enumeration_settings
        :param point_name: String point name
        :return: Point type (str)
        """
        hardcoded_types = self._read_hardcoded_types()
        known_types = self.db_connection.get_all_point_types()
        if point_name in hardcoded_types:
            return known_types[hardcoded_types[point_name]]

        point_dict = self.json_dict[point_name]

        if "Analog Representation" in point_dict:
            return_type = point_dict["Analog Representation"].lower()
            units = point_dict["Engineering Units"]
            factor = point_dict["# of decimal places"]
            type_name = return_type + units + factor
            new_type = PointType(type_name, return_type)
            new_type.units = units
            new_type.factor = int(factor)
        else:
            return_type = "enumerated"
            enumeration_settings = point_dict["Text Table"][1]
            type_name = return_type + ",".join(enumeration_settings)
            new_type = PointType(type_name, return_type)
            new_type.enumeration_settings = enumeration_settings

        self.db_connection.add_point_type(new_type)
        known_types[new_type.name] = new_type
        return new_type


    def _add_point_values(self):
        """
        Loops over all points and all values for points, adds to db
        :return: None
        """
        df = self.siemens_data
        keep_cols = ['Date', 'Time']
        point_names = [x for x in list(df.columns.values) if x not in keep_cols]
        # first melt the point name headers into the table
        # so that point name is now a row variable, not a header
        df = pd.melt(df, id_vars=['Date', 'Time'], value_vars=point_names, var_name='pointname', value_name='pointvalue')
        print("Melted")
        # Next combine the date and time columns into one 
        df['pointtimestamp'] = df['Date'] + ' ' + df['Time']

        print("Timestamps Combined")


        # transform pointnames to pointids based on the mapping that we constructed earlier
        # get rid of cases where we get a null point id- means we couldn't map a type to the point
        df['pointid'] = df['pointname'].apply(self._map_point_names_id)

        df.dropna(axis=0, how='any', inplace=True)
        print('Null Points Dropped')

        df['pointid'] = df['pointid'].astype(int)
        print("Points Mapped")

        #finally get our formatted point values by inputting the row into format_value
        if df.empty:
            # Just check to make sure we don't have an empty df- otherwise it errors here if we do
            print("Invalid insert- double check that the points are successfully getting inserted")
            return
        df['pointvalue'] = df.apply(self._format_value, axis=1)
        #replace all NaNs with None for sql
        print("Values Formatted")

        # drop all of the old cols
        df.drop(['Date', 'Time', 'pointname'], axis=1, inplace=True)
        # Now format it to go into the sql
        df = df[['pointvalue', 'pointtimestamp', 'pointid']]
        
        print("COPY FROM FORMATTING FINISHED")
        self.db_connection.bulk_add_point_values(df)

    def _map_point_names_id(self, name):
        try:
            return self.points[name].id
        except KeyError:
            return None

    def _format_value(self, row):
        """
        Makes every given value into an integer for storage in db
        :param row: pandas dataframe containing a raw_value and a point_name
        :return: Formatted value as an int corresponding to the original data
        """
        # TODO error catching if value not type expected, what if there is a problem value not in that list
        point_name = row['pointname']
        raw_value = row['pointvalue']
        point = self.points[point_name]
        problem_values = ["data loss", "no data", "nan", "null"]
        if (isinstance(raw_value, str) and raw_value.lower() in problem_values) or pd.isnull(raw_value):
            formatted_value = 'None'
        elif point.point_type.return_type == "enumerated":
            formatted_value = point.point_type.enumeration_settings.index(raw_value)
            # TODO if it doesn't have that value???, what if value is 'closed' and we expected 'on'/'off'
        elif point.point_type.return_type == "float":
            formatted_value = float(raw_value) * 10 ** point.point_type.factor
            formatted_value = round(formatted_value)
        else:  # it's an int!
            formatted_value = int(raw_value)
        return formatted_value


def main(building, csv_file):
    """
    Read in individual file and add all subpoints to DB
    :return:
    """
    transformed_file = transform_file(get_data_resource("csv_files/"+csv_file))

    sr = SiemensReader(transformed_file, building, Sources.SIEMENS)
    sr.add_to_db()
    sr.db_connection.close_connection()

def stream_main(building, input_string):
    transformed_file = transform_string(input_string)
    sr = SiemensReader(transformed_file, building, Sources.SIEMENS)
    sr.add_to_db()
    sr.db_connection.close_connection()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        given_building = sys.argv[1]  # building should be as spelled in the data description file name
        given_csv_file = sys.argv[2]
        main(given_building, given_csv_file)
    elif len(sys.argv) > 1 and not sys.stdin.isatty():
        given_building = sys.argv[1]
        stream_main(given_building, sys.stdin.read())
    else:
        print("Requires a building name and a csv file parameter")
