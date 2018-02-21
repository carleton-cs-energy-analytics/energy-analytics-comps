"""
Generates rooms for points in a given building
"""
from src.datareaders.database_connection import DatabaseConnection
import sys


class RoomTagger:
    def __init__(self, building_name):
        self.db_connection = DatabaseConnection()
        self.building_id = self.db_connection.get_building_id(building_name)
        self.generate_rooms()

    def generate_rooms(self):
        points = self.db_connection.get_point_names_in_building(self.building_id)
        for point in points:
            name = point[0]
            pid = point[1]
            rid = point[2]
            room_name = self.parse_room_name(name)
            if room_name:
                room_id = self.db_connection.add_unique_room(room_name, self.building_id)
                if rid == room_id:
                    continue
                self.db_connection.update_point_room(str(pid), str(room_id))

    def parse_room_name(self, name):
        room_identifier = "RM"
        parts = name.split(".")
        if len(parts) == 3:
            full_name = parts[1]
            if room_identifier in full_name:
                return full_name.replace(room_identifier, "")
        return False


if __name__ == '__main__':
    building = 'Evans'
    if len(sys.argv) > 1:
        building = sys.argv[1]
    RoomTagger(building)
