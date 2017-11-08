from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.siemens.siemens_data import SiemensData
from src.datareaders.data_object_holders import Point, PointType
from json import load as json_load

class SiemensReader:
    def __init__(self, file_name, building, source):
        self.file_path = get_data_resource("better_csv_files/"+file_name)
        self.building_name = building
        self.source = source
        self.db_connection = DatabaseConnection()
        self.siemens_data = SiemensData()
        self.siemens_data.read_csv(self.file_path)
        json_file = open(get_data_resource("csv_descriptions/testPointJson_LDC.json"), "r")
        self.json_dict = json_load(json_file)

    def add_to_db(self):
        self._add_building()

        for point_name in self.siemens_data.data.columns[2:]:
            room_name = self._parse_room(point_name)
            point_type = self._get_point_type(point_name)
            description = self.json_dict[point_name]["Descriptor"]

            point = Point(point_name, room_name, self.building_name, self.source, point_type, description)

            self.db_connection.add_unique_room(room_name, self.building_name)
            self.db_connection.add_unique_point(point)

    def _add_building(self):
        self.db_connection.add_unique_building(self.building_name)

    def _parse_room(self, point_name):
        # print(point_name)
        l = point_name.split(".")
        potential_room = l[1]
        # IF potential room is room, add it
        # ELSE find none room for this building
        # TODO add some sort of smart knowledge about whether or not this is a room
        print("ROOM??", potential_room)
        return potential_room

    def _read_type_codes(self):
        """
        Reads code - type pairs from a given file
        """
        known_type_codes = {}
        return known_type_codes

    def _get_point_type(self, point_name):
        """
        Returns the point type for the given name
        If from the known type codes, name will be reasonable
        If new type, name will be a concatenation of return_type and units/enumeration_settings
        """
        type_codes = self._read_type_codes()
        known_types = self.db_connection.get_all_point_types()
        if point_name in type_codes:
            return known_types[type_codes[point_name]]
        point_dict = self.json_dict[point_name]
        if "Analog Representation" in point_dict:
            return_type = point_dict["Analog Representation"]
            units = point_dict["Engineering Units"]
            type_name = return_type + units
            new_type = PointType(type_name, return_type)
            new_type.units = units
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
        """
        pass


def main():
    sr = SiemensReader("LDC.AUDIT.TRENDRPT1_171016.csv", "LDC", Sources.SIEMENS)
    sr.add_to_db()

if __name__ == '__main__':
    main()