"""
Reads a given csv file and adds all information to the database
"""
from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.data_object_holders import Point, PointType
from src.datareaders.siemens.nameParser import tagName
from src.datareaders.siemens.siemens_parser import transform_file, transform_string
from json import load as json_load
import sys
import pandas as pd
import time


class SiemensReader:
    def __init__(self, input_stream):
        self.source = Sources.SIEMENS
        self.db_connection = DatabaseConnection()
        self.siemens_data = pd.read_csv(input_stream)
        tag_json = open(get_data_resource("csv_descriptions/PointDecoder.json"))
        self.tag_dict = json_load(tag_json)
        self.points_with_ids = {}

    def add_to_db(self):
        """
        Adds building, rooms, point types, and point to the database
        :return: None
        """
        finish_lst = []
        cant_finish_lst = []
        for point_name in self.siemens_data.columns[2:]:
            tags = tagName(point_name, self.tag_dict)
            if tags is None:
                cant_finish_lst.append("No tags for point " + point_name)
                continue
            building_id, building_name = self._add_building(tags)
            room_id = self._add_room(tags, building_name, building_id)
            equipment_id = self._add_equipment_box(tags)
            point_type_id, point_type = self._add_point_type(tags)
            description = self._make_point_description(tags)
            point = Point(point_name, room_id, building_id, self.source, point_type_id, description, equipment_id)
            point.point_type = point_type

            point_id = self.db_connection.add_unique_point(point)
            point.id = point_id
            self.points_with_ids[point.name] = point
            finish_lst.append("Finished for point "+point_name)

        for item in finish_lst:
            print(item)

        for item in cant_finish_lst:
            print(item)

        print("Was able to successfully add {} points".format(len(finish_lst)))
        print("Was NOT able to add {} points".format(len(cant_finish_lst)))

        self._add_point_values()

    def _add_building(self, tags):
        """
        Add unique building from the building tag of a point
        Only adds building if not in DB, adds dummy "Carleton Campus" building if no building tag
        :param tags: a dictionary of tags for a point
        :return: The building id (int) added to the database
        """
        building = "Carleton Campus"  # dummy building
        if "Building" in tags:
            building = tags["Building"][0]

        building_id = self.db_connection.add_unique_building(building)
        return building_id, building

    def _add_room(self, tags, building_name, building_id):
        """
        Add unique room -- only adds if room not already in DB
        :param tags: a dictionary of tags for a point
        :param building_name: Building name of point (string)
        :return: Room id (int)
        """
        room = "{}_Dummy_Room".format(building_name)
        if "ROOM" in tags:
            room = tags["ROOM"][0]

        room_id = self.db_connection.add_unique_room(room, building_id)
        return room_id

    def _add_equipment_box(self, tags):
        """
        Add unique equipment box -- only adds if not in DB
        :param tags: a dictionary of tags for a point
        :return: equipment box id (int)
        """
        if "Equipment" in tags:
            description = self.tag_dict[tags["Equipment"][0]]["descriptor"]
            equipment_name = tags["Equipment"][0]
            if len(tags["Equipment"]) > 1:
                equipment_name += tags["Equipment"][1]
            equipment_id = self.db_connection.add_unique_equipment_box(equipment_name, description)
            return equipment_id
        return None

    def _make_point_description(self, tags):
        """
        Creates the point description as a concatenation of the descriptions of its tags
        :param tags: a dictionary of the tags for a point
        :return: a string description
        """
        description = ""
        if "Measurement" in tags:
            description += self.tag_dict[tags["Measurement"][0]]["descriptor"]
        if "Set Point" in tags:
            description += self.tag_dict[tags["Set Point"][0]]["descriptor"]
        if "Equipment" in tags:
            description += " in " + self.tag_dict[tags["Equipment"][0]]["descriptor"]
        if "Room" in tags:
            description += " in Room " + tags["ROOM"][0]
        if "Building" in tags:
            description += " in " + self.tag_dict[tags["Building"][0]]["descriptor"]
        return description

    def _get_point_type(self, tags):
        """
        Gets the measurement or set point type tag in the dictionary of tags
        :param tags: a dictionary of tags for a point
        :return: the measurement or set point tag (should only be one)
        """
        try:
            if "Measurement" in tags:
                return tags["Measurement"][0]
            else:
                return tags["Set Point"][0]
        except KeyError:
            print("This point does not have a type")
            return None

    def _add_point_type(self, tags):
        """
        Gets point type information from tags and adds to databse
        :param tags: a dictionary of tags for a point
        :return: point type id (int)
        """
        point_type_name = self._get_point_type(tags)
        if self.tag_dict[point_type_name]["isEnumerated"] == "True":
            point_type = PointType(point_type_name, "enumerated")
            point_type.enumeration_values = self.tag_dict[point_type_name]["units"][5:].split("/")
        else:
            point_type = PointType(point_type_name, "float")
            point_type.units = self.tag_dict[point_type_name]["units"]
            point_type.factor = 5  # No longer getting this information, everything should be less than this

        point_type_id = self.db_connection.add_unique_point_type(point_type)
        return point_type_id, point_type

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

        # finally get our formatted point values by inputting the row into format_value
        if df.empty:
            # Just check to make sure we don't have an empty df- otherwise it errors here if we do
            print("Invalid insert- double check that the points are successfully getting inserted")
            return
        df['pointvalue'] = df.apply(self._format_value, axis=1)
        # replace all NaNs with None for sql
        print("Values Formatted")

        # drop all of the old cols
        df.drop(['Date', 'Time', 'pointname'], axis=1, inplace=True)
        # Now format it to go into the sql
        df = df[['pointvalue', 'pointtimestamp', 'pointid']]
        
        print("COPY FROM FORMATTING FINISHED")
        self.db_connection.bulk_add_point_values(df)

    def _map_point_names_id(self, name):
        try:
            return self.points_with_ids[name].id
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
        point = self.points_with_ids[point_name]
        problem_values = ["data loss", "no data", "nan", "null"]
        if (isinstance(raw_value, str) and raw_value.lower() in problem_values) or pd.isnull(raw_value):
            formatted_value = 'None'
        elif point.point_type.return_type == "enumerated":
            formatted_value = point.point_type.enumeration_values.index(raw_value)
            # TODO if it doesn't have that value???, what if value is 'closed' and we expected 'on'/'off'
        elif point.point_type.return_type == "float":
            formatted_value = float(raw_value) * 10 ** point.point_type.factor
            formatted_value = round(formatted_value)
        else:  # it's an int!
            formatted_value = int(raw_value)
        return formatted_value


def main(csv_file):
    """
    Read in individual file and add all subpoints to DB
    :return:
    """
    transformed_file = transform_file(get_data_resource("csv_files/"+csv_file))

    sr = SiemensReader(transformed_file)
    sr.add_to_db()
    sr.db_connection.close_connection()


def stream_main(input_string):
    transformed_file = transform_string(input_string)
    sr = SiemensReader(transformed_file)
    sr.add_to_db()
    sr.db_connection.close_connection()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        given_csv_file = sys.argv[1]
        main(given_csv_file)
    elif not sys.stdin.isatty():
        stream_main(sys.stdin.read())
    else:
        print("Requires a csv file parameter")
