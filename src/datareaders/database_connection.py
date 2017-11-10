'''
This is the only file that has a connection to the database
'''
import psycopg2
from src.datareaders.data_object_holders import PointType
from src.datareaders.data_connection_params import params
class DatabaseConnection:

    def __init__(self):
        '''
        Construction takes no parameters, automatically opens connection
        '''
        db = None
        conn = None
        self.open_connection()

    def open_connection(self):
        '''
        Opens connection to DB
        :return: None
        '''
        try:
            self.conn = psycopg2.connect(**params)
            self.db = self.conn.cursor()
            print("Database Connected")
        except:
            print("Database Connection Failed")

    def close_connection(self):
        '''
        Closes connection to DB
        :return: None
        '''
        self.db.close()
        self.conn.close()

    def execute_and_commit(self, *args):
        '''
        Takes in any number of execute arguments
        Ensures that our execute and commit statements are always paired
        :param args: SQL String, if any "(%s)" in string -- needs (fill_string,)
               Args match db.execute(args)
        :return: None
        '''
        self.db.execute(*args)
        self.conn.commit()

    def add_building(self, building_name):
        '''
        Adds a given building to the buildings table of the database
        :param building_name: Building name (str)
        :return: None
        '''
        self.execute_and_commit("INSERT INTO Buildings(Name) VALUES (%s);", (building_name,))

    def add_room(self, room_name, building_name):
        '''
        Adds a room to Rooms table with building name as foreign key
        :param room_name: str room name
        :param building_name: str building name
        :return: None
        '''
        building_id = self.get_building_id(building_name)
        self.execute_and_commit("INSERT INTO Rooms(Name, BuildingID) VALUES (%s, %s);", (room_name, building_id))

    def add_point_type(self, point_type):
        '''
        Adds a point type to the point type table
        :param point_type: PointType class, has values name, units, return type, and factor
        :return: None
        '''
        self.execute_and_commit("INSERT INTO PointTypes(Name, Units, ReturnType, Factor) VALUES (%s, %s, %s, %s);",
                        (point_type.name, point_type.get_units_placeholder(), point_type.return_type,
                         self.formatSQLNone(point_type.factor)))

    def add_point(self, point):
        '''
        Adds point to Points table
        :param point: Point class has name, room_id, type_id, source, and description
        :return: None
        '''
        room_id = self.get_room_id(point.room, point.building)
        type_id = self.get_point_type_id(point.point_type)
        self.execute_and_commit("INSERT INTO Points(Name, RoomID, PointTypeID, PointSourceID, Description) VALUES (%s, %s, "
                        "%s, %s, %s);", (point.name, room_id, type_id, point.source, point.description))

    def add_point_value(self, timestamp, point, value):
        '''
        Adds a value for given point at specified timestamp
        :param timestamp: Timestamp of point, str
        :param point: Point class
        :param value: Data value to be recorded for given timestamp, point
               Encoded as an integer
        :return: None
        '''
        # TODO make sure we convert to value before calling this
        point_id = self.get_point_id(point)
        self.execute_and_commit("INSERT INTO PointValues (PointTimestamp, PointID, PointValue) VALUES "
                        "(%s, %s, %s);", (timestamp, point_id, value))

    # get_-_id methods return the ID of an object if it is in the database, or None if not
    def get_building_id(self, building_name):
        '''
        Looks in DB for builiding with building name
        :param building_name: Building name, str
        :return: Building id if exists, None otherwise
        '''
        self.db.execute("SELECT ID from Buildings where Name = (%s);", (building_name,))
        id = self.db.fetchone()
        if id is None:
            return None
        else:
            return id[0]

    def get_room_id(self, room_name, building_name):
        '''
        Looks in DB for room with room name
        :param room_name: Room name, str
        :param building_name: Building name, str
        :return: Room id if exists, None otherwise
        '''
        building_id = self.get_building_id(building_name)
        self.db.execute("SELECT ID, Name from Rooms where Name = (%s) AND BuildingID = (%s);", (room_name, building_id))
        id = self.db.fetchone()
        if id is None:
            return None
        else:
            return id[0]

    def get_point_type_id(self, point_type):
        '''
        Looks in DB for point type
        :param point_type: PointType class
        :return: PointType id if exists, None otherwise
        '''
        self.db.execute("SELECT ID from PointTypes where Name = (%s);", (point_type.name,))
        id = self.db.fetchone()
        if id is None:
            return None
        else:
            return id[0]

    def get_point_id(self, point): # only need to use name and room/building combo
        '''
        Looks in DB for point
        :param point: Point class
        :return: Point id if exists, None otherwise
        '''
        self.db.execute("SELECT ID from Points where Name = (%s);", (point.name, ))
        id = self.db.fetchone()
        if id is None:
            return None
        else:
            return id[0]

    # addUnique methods add object to database only if it is not already in the database
    def add_unique_building(self, building_name):
        '''
        Add unique building only adds building to DB if doesn't exist already
        :param building_name: Building name, str
        :return: None
        '''
        if self.get_building_id(building_name) is None:
            self.add_building(building_name)

    def add_unique_room(self, room_name, building_name):
        '''
        Add unique room only adds room to DB if doesn't already exist
        :param name: Room name, str
        :param building_name: Building name, str
        :return: None
        '''
        if self.get_room_id(room_name, building_name) is None:
            self.add_room(room_name, building_name)

    def add_unique_point_type(self, point_type):
        '''
        Add unique point type only adds point type to DB if doesn't already exist
        :param point_type: PointType class
        :return: None
        '''
        if self.get_point_type_id(point_type) is None:
            self.add_point_type(point_type)

    def add_unique_point(self, point):
        '''
        Add unique point only adds point to DB if doesn't already exist
        :param point: Point class
        :return: None
        '''
        if self.get_point_id(point) is None:
            self.add_point(point)

    # getAll methods select * from database and return as a dictionary with key as name
    def get_all_point_types(self):
        '''
        Grabs all known Point Types from database
        :return: dictionary {name: point type information}
        '''
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


    # TODO might not need this anymore now that we are using %s again
    def formatSQLNone(self, value):
        '''
        SQL doesn't like None, but it likes NULL
        :param value: anything
        :return: "NULL" if value None, value otherwise
        '''
        if value is None:
            return "NULL"
        else:
            return value
