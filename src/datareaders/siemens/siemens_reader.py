"""
Reads a given csv file and adds all information to the database
"""
from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.data_object_holders import Point, PointType
from src.datareaders.siemens.siemens_parser import transform_file
from json import load as json_load
from sys import argv
import pandas as pd


class SiemensReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.source = Sources.SIEMENS
        self.db_connection = DatabaseConnection()
        self.siemens_data = pd.read_csv(file_path, dtype=object)
        tag_json = open(get_data_resource("csv_descriptions/PointDecoder.json"))
        self.tag_dict = json_load(tag_json)

    def add_to_db(self):
        """
        Adds building, rooms, point types, and point to the database
        :return: None
        """
        finish_lst = []
        cant_finish_lst = []
        points_with_ids = []
        for point_name in self.siemens_data.columns[2:]:
            try:
                tags = {}  # TODO: get tags
                building_id, building_name = self._add_building(tags)
                room_id = self._add_room(tags, building_name, building_id)
                point_type_id, point_type = self._add_point_type(tags)
                description = self._make_point_description(tags)

                point = Point(point_name, room_id, building_id, self.source, point_type_id, description)
                point.point_type = point_type

                point_id = self.db_connection.add_unique_point(point)
                point.id = point_id
                points_with_ids.append(point)
                finish_lst.append("Finished for point "+point_name)
            except KeyError:
                cant_finish_lst.append("Don't know type of "+point_name)

        for item in finish_lst:
            print(item)

        for item in cant_finish_lst:
            print(item)

        print("Was able to successfully add {} points".format(len(finish_lst)))
        print("Was NOT able to add {} points".format(len(cant_finish_lst)))

        self._add_point_values(points_with_ids)

    def _add_building(self, tags):
        """
        Add unique building from the building tag of a point
        Only adds building if not in DB, adds dummy "Carleton Campus" building if no building tag
        :param tags: a dictionary of tags for a point
        :return: The building id (int) added to the database
        """
        building = "Carleton Campus"  # dummy building
        if "building" in tags:
            building = tags["building"]  # TODO: might change key

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
        if "room" in tags:
            room = tags["room"]  # TODO: might change key

        room_id = self.db_connection.add_unique_room(room, building_id)
        return room_id

    def _make_point_description(self, tags):
        """
        Creates the point description as a concatenation of the descriptions of its tags
        :param tags: a dictionary of the tags for a point
        :return: a string description
        """
        description = ""
        for key, value in tags.items():
            description += self.tag_dict[value]["descriptor"] + ", "
        description = description[:len(description)-2]
        return description

    def _get_point_type(self, tags):
        """
        Gets the measurement or set point type tag in the dictionary of tags
        :param tags: a dictionary of tags for a point
        :return: the measurement or set point tag (should only be one)
        """
        try:
            if "measurement" in tags:
                return tags["measurement"]  # TODO: might change key
            else:
                return tags["set point"]  # TODO: might change key
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
        # TODO: differentiate between enum and float
        if self.tag_dict[point_type_name]["return type"] == "enum":
            point_type = PointType(point_type_name, "enumerated")
            point_type.enumeration_values = self.tag_dict[point_type_name]["units"].split(",")
        else:
            point_type = PointType(point_type_name, "float")  # TODO: get return type
            point_type.units = self.tag_dict[point_type_name]["units"]
            point_type.units = self.tag_dict[point_type_name]["factor"]

        point_type_id = self.db_connection.add_unique_point_type(point_type)
        return point_type_id, point_type

    def _add_point_values(self, points_with_ids):
        """
        Loops over all points and all values for points, adds to db
        :return: None
        """
        point_index = 0
        for point in points_with_ids:
            print("starting point {}, number {}".format(point.name, point_index))
            try:
                for i in range(len(self.siemens_data[point.name])):
                    date = self.siemens_data.Date[i]
                    time = self.siemens_data.Time[i]
                    raw_data = self.siemens_data[point.name][i]
                    formatted_value = self._format_value(point, raw_data)
                    self.db_connection.add_unique_point_value(timestamp=date+" "+time, point_id = point.id,
                                                              value=formatted_value)
                point_index += 1
                print("finished point {}".format(point.name))
            except ValueError:
                print("point {} failed to go in with value {}".format(point.name, raw_data))
                continue

    def _format_value(self, point, raw_value):
        """
        Makes every given value into an integer for storage in db
        :param point: Point name
        :param raw_value: Value as given in csv
        :return: Formatted value as an int corresponding to the original data
        """
        # TODO error catching if value not type expected, what if there is a problem value not in that list
        problem_values = ["data loss", "no data", "nan", "null"]
        if (isinstance(raw_value, str) and raw_value.lower() in problem_values) or pd.isnull(raw_value):
            formatted_value = None
        elif point.point_type.return_type == "enumerated":
            formatted_value = point.point_type.enumeration_values.index(raw_value)
            # TODO if it doesn't have that value???, what if value is 'closed' and we expected 'on'/'off'
        elif point.point_type.return_type == "float":
            formatted_value = float(raw_value) * 10 ** point.point_type.factor
            formatted_value = round(formatted_value)
        else:  # it's an int!
            formatted_value = int(raw_value)

        return formatted_value


def test_insert():
    # TODO: delete this, just for note purposes
    # this works if the self.siemens_data = ... line above is commented out (don't need to csv)
    tags = {"building":"TEST BUILDING", "room": "TEST ROOM", "measurement": "TEST TYPE"}
    sr = SiemensReader("")
    building_id, building_name = sr._add_building(tags)
    room_id = sr._add_room(tags, building_name, building_id)
    point_type_id, point_type = sr._add_point_type(tags)
    description = sr._make_point_description(tags)

    point = Point("TEST POINT", room_id, building_id, Sources.SIEMENS, point_type_id, description)
    point.point_type = point_type

    point_id = sr.db_connection.add_unique_point(point)
    print("Inserted point: " + str(point_id))

    sr.db_connection.add_unique_point_value(timestamp="2016-08-18 00:45:00", point_id=point_id,
                                            value=None)
    sr.db_connection.add_unique_point_value(timestamp="2016-08-18 00:30:00", point_id=point_id,
                                            value=point.point_type.enumeration_values.index("ON"))
    sr.db_connection.add_unique_point_value(timestamp="2016-08-18 00:15:00", point_id=point_id,
                                            value=point.point_type.enumeration_values.index("OFF"))


def main(building, csv_file):
    """
    Read in individual file and add all subpoints to DB
    :return:
    """
    transform_file(get_data_resource("csv_files/"+csv_file))

    sr = SiemensReader(get_data_resource("better_csv_files/"+csv_file))
    sr.add_to_db()
    sr.db_connection.close_connection()


if __name__ == '__main__':
    test_insert()
    # if len(argv) > 2:
    #     given_building = argv[1]  # building should be as spelled in the data description file name
    #     given_csv_file = argv[2]
    #     main(given_building, given_csv_file)
    # else:
    #     print("Requires a building name and a csv file parameter")
