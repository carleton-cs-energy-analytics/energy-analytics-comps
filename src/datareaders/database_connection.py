import psycopg2
from src.datareaders.data_object_holders import PointType
from src.datareaders.data_connection_params import params
class DatabaseConnection:
    # some connection information
    db = None

    def __init__(self):
        try:
            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            print("database connected")

        except:
            print("Connection Failed")

    def add_building(self, name):
        self.db.execute("INSERT INTO Buildings(Name) VALUES (%s);", (name))

    def add_room(self, name, building_name):
        building_id = self.get_building_id(building_name)
        self.db.execute("INSERT INTO Rooms(Name, BuildingID) VALUES (%s, %i);", (name, building_id))

    def add_point_type(self, point_type):
        self.db.execute("INSERT INTO PointTypes(Name, Units, ReturnType, Factor) VALUES (%s, %s, %s, %i);",
                        (point_type.name, point_type.get_units_placeholder(), point_type.return_type,
                         point_type.factor))

    def add_point(self, point):
        room_id = self.get_room_id(point.room, point.building)
        type_id = self.get_point_type_id(point.point_type)
        self.db.execute("INSERT INTO Points(Name, RoomID, PoinTypeID, PointSourceID, Description) VALUES (%s, %i, "
                        "%i, $i, $s);", (point.name, room_id, type_id, point.source, point.description))

    def add_point_value(self, timestamp, point, value):
        point_id = self.get_point_id(point)
        self.db.execute("INSERT INTO PointValues (PointTimestamp, PointID, PointValue) VALUES (%s, %i, %i);",
                        (timestamp, point_id, value))

    # get_-_id methods return the ID of an object if it is in the database, or None if not

    def get_building_id(self, name):
        self.db.execute("SELECT ID from Buildings where Name = '" + name + "'")
        return self.db.fetchone()

    def get_room_id(self, name, building_name):
        building_id = self.get_building_id(building_name)
        self.db.execute("SELECT ID from Rooms where Name = '" + name + "' AND BuildingID = " + str(building_id))
        return self.db.fetchone()

    def get_point_type_id(self, point_type):
        self.db.execute("SELECT ID from PointTypes where Name = '" + point_type.name)
        return self.db.fetchone()

    def get_point_id(self, point): # only need to use name and room/building combo
        self.db.execute("SELECT ID from Points where Name = '" + point.name)
        return self.db.fetchone()

    # addUnique methods add object to database only if it is not already in the database

    def add_unique_building(self, name):
        if (self.get_building_id(name) is None):
            self.add_building(name)

    def add_unique_room(self, name, building_name):
        if (self.get_room_id(name, building_name) is None):
            self.add_room(name, building_name)

    def add_unique_point_type(self, point_type):
        if (self.get_point_type_id(point_type) is None):
            self.add_point_type(point_type)

    def add_unique_point(self, point):
        if (self.get_point_id(point) is None):
            self.add_point(point)

    # getAll methods select * from database and return as a dictionary with key as name

    def get_all_point_types(self):
        known_types = {}
        self.db.execute("SELECT * FROM PointTypes")
        next_entry = self.db.fetchone()
        while next_entry is not None:
            return_type = next_entry[2]
            this_type = PointType(next_entry[0], return_type)
            if return_type == "enumerated":
                this_type.enumeration_settings = next_entry[1].split(",")
            else:
                this_type.units = next_entry[1]
            known_types[next_entry[0]] = this_type
            next_entry = self.db.fetchone()
        return known_types

