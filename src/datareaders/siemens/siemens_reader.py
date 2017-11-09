'''
Reads a given csv file and adds all information to the database
'''
from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.siemens.siemens_data import SiemensData
from src.datareaders.data_object_holders import Point, PointType
from src.datareaders.siemens.siemens_parser import transform_file
from json import load as json_load

class SiemensReader:
    def __init__(self, file_path, building, source):
        self.file_path = file_path
        self.building_name = building
        self.source = source
        self.db_connection = DatabaseConnection()
        self.siemens_data = SiemensData()
        self.siemens_data.read_csv(self.file_path)
        json_file = open(get_data_resource("csv_descriptions/testPointJson_{}.json".format(building)), "r")
        self.json_dict = json_load(json_file)

    def add_to_db(self):
        '''
        Adds building, rooms, point types, and point to the database
        :return: None
        '''
        self._add_building()
        finish_lst = []
        cant_finish_lst = []
        for point_name in self.siemens_data.data.columns[2:]:
            try:
                room_name = self._add_room(point_name)
                point_type = self._get_point_type(point_name)
                description = self.json_dict[point_name]["Descriptor"]

                point = Point(point_name, room_name, self.building_name, self.source, point_type, description)

                self.db_connection.add_unique_point(point)
                finish_lst.append("Finished for point "+point_name)
            except KeyError as e:
                cant_finish_lst.append("Don't know type of "+point_name)

        for item in finish_lst:
            print(item)

        for item in cant_finish_lst:
            print(item)

        print("Was able to successfully add {} points".format(len(finish_lst)))
        print("Was NOT able to add {} points".format(len(cant_finish_lst)))

    def _add_building(self):
        '''
        Add unique building -- only adds if building not already in DB
        :return: None
        '''
        self.db_connection.add_unique_building(self.building_name)

    def _add_room(self, point_name):
        '''
        Add unique room -- only adds if room not already in DB
        :param point_name: String of point name --> not used but should be if we want real rooms!
        :return: Room name (str)
        '''
        room = "{}_Room".format(self.building_name)
        # TODO Actually get room information from point information
        # IF potential room is room, add it
        # ELSE find none room for this building
        self.db_connection.add_unique_room(room, self.building_name)
        return room

    def _read_type_codes(self):
        """
        Reads code - type pairs from a given file
        """
        # TODO Explain what a type code is @kiya has told me like 10 times and i'm still lost
        known_type_codes = {}
        return known_type_codes

    def _get_point_type(self, point_name):
        """
        Returns the point type for the given name
        If from the known type codes, name will be reasonable
        If new type, name will be a concatenation of return_type and units/enumeration_settings
        :param point_name: String point name
        :return: Point type (str)
        """
        type_codes = self._read_type_codes()
        known_types = self.db_connection.get_all_point_types()
        if point_name in type_codes:
            return known_types[type_codes[point_name]]

        # TODO Remove this once we can successfully get point types
        # Returns dummy point type if we don't know the point
        # if point_name not in self.json_dict:
        #     new_type = PointType("Point_{}_Type_Unknown".format(point_name), "string") # TODO Ask Kiya what this should be

        point_dict = self.json_dict[point_name]

        if "Analog Representation" in point_dict:
            return_type = point_dict["Analog Representation"]
            units = point_dict["Engineering Units"]
            factor = point_dict["# of decimal places"]
            type_name = return_type + units
            new_type = PointType(type_name, return_type)
            new_type.units = units
            new_type.factor = factor
        else:
            return_type = "enumerated"
            enumeration_settings = point_dict["Text Table"][1]
            type_name = return_type + ",".join(enumeration_settings)
            new_type = PointType(type_name, return_type)
            new_type.enumeration_settings = enumeration_settings

        self.db_connection.add_point_type(new_type)
        known_types[new_type.name] = new_type
        return new_type

    def _populate_table_with_known_types(self):  # RUN ONLY ONCE
        """
        Adds known types from a file into the database table. Meant to be called only once
        This will be a hardcoded insert most likely in the db_scheme
        """
        # TODO --- Delete???
        pass


def main():
    '''
    Read in individual file and add all subpoints to DB
    :return:
    '''
    csv_file = "SAYLES.AUDIT.TRENDRPT_171016.csv"

    transform_file(get_data_resource("csv_files/"+csv_file))

    sr = SiemensReader(get_data_resource("better_csv_files/"+csv_file), "Sayles", Sources.SIEMENS)
    sr.add_to_db()
    sr.db_connection.close_connection()

if __name__ == '__main__':
    main()