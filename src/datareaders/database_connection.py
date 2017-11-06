import psycopg2
from src.datareaders.data_object_holders import PointType

class DatabaseConnection:
    # some connection information
    db = None

    def __init__(self):
        db_connection = psycopg2.connect("magic")
        db = db_connection.cursor()
        pass

    # add methods add object to database

    def addBuilding(self, name):
        pass

    def addRoom(self, name, building_name):
        pass

    def addPointType(self, point_type):
        pass

    def addPoint(self, point):
        pass

    def addPointValue(self, timestamp, point_id, value):
        pass

    # getID methods return the ID of an object if it is in the database, or None if not

    def getIDBuilding(self, name):
        pass

    def getIDRoom(self, name, building_id):
        pass

    def getIDPointType(self, point_type):
        pass

    def getIDPoint(self, point): # only need to use name and room/building combo
        pass

    # addUnique methods add object to database only if it is not already in the database

    def addUniqueBuilding(self, name):
        pass

    def addUniqueRoom(self, name, building_name):
        pass

    def addUniquePointType(self, point_type):
        pass

    def addUniquePoint(self, point):
        pass

    # getAll methods select * from database and return as a dictionary with key as name

    def getAllPointTypes(self):
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

