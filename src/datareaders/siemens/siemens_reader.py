from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.siemens.siemens_data import SiemensData
from src.datareaders.siemens.add_points import add_point_to_db
from src.datareaders.data_object_holders import Point

class SiemensReader:
    def __init__(self, file_name, building, source):
        self.file_path = get_data_resource("better_csv_files/"+file_name)
        self.building_name = building
        self.source = source
        self.db_connection = DatabaseConnection()
        self.siemens_data = SiemensData()
        self.siemens_data.read_csv(self.file_path)

    def add_to_db(self):
        self._add_building()

        for point_name in self.siemens_data.data.columns[2:]:
            room_name = self._parse_room(point_name)
            self.db_connection.addUniqueRoom(room_name, self.building_name)
            add_point_to_db(point_name, room_name, self.building_name, self.source)

    def _add_building(self):
        self.db_connection.addUniqueBuilding(self.building_name)

    def _parse_room(self, point_name):
        # print(point_name)
        l = point_name.split(".")
        potential_room = l[1]
        # IF potential room is room, add it
        # ELSE find none room for this building
        # TODO add some sort of smart knowledge about whether or not this is a room
        print("ROOM??", potential_room)
        return potential_room


def main():
    sr = SiemensReader("140708-141112_LDC.AUDIT.TRENDRPT1.csv", "LDC", Sources.SIEMENS)
    sr.add_to_db()

if __name__ == '__main__':
    main()