"""
Deduplicates buildings (where siemens calls something Libe and lucid calls it Library)
"""
from src.datareaders.database_connection import DatabaseConnection


class BuildingDeduplicator:
    building_mapper = {
        'Libe': 5,
        'Rec': 9,
        'Cassat Hall/James Hall': 40
    }
    def __init__(self):
        self.db_connection = DatabaseConnection()
        self.raw_buildings = self.db_connection.get_buildings()
        self.construct_buildings()
        self.deduplicate()

    def construct_buildings(self):
        self.buildings = {}
        for building in self.raw_buildings:
            bid = building[0]
            name = building[1]
            self.buildings[name] = bid

    def deduplicate(self):
        for building in self.raw_buildings:
            bid = building[0]
            name = building[1]
            new_id = building[0]
            cleaned_name = name.strip()
            cleaned_name = cleaned_name.title()
            if cleaned_name in self.building_mapper:
                new_id = self.building_mapper[cleaned_name]
            else:
                hallified = cleaned_name + " Hall"
                if hallified in self.buildings:
                    new_id = self.buildings[hallified]
                if cleaned_name in self.buildings:
                    new_id = self.buildings[cleaned_name]
            if new_id != bid:
                self.db_connection.update_room_building_ids(bid, new_id)



if __name__ == '__main__':
    BuildingDeduplicator()
