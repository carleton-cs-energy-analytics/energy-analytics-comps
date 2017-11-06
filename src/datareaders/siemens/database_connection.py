class DatabaseConnection:
    # some connection information

    def __init__(self):
        pass

    # add methods add object to database

    def addBuilding(self, name):
        pass

    def addRoom(self, name, building_id):
        pass

    def addPointType(self, name, return_type, units, factor):
        pass

    def addPoint(self, name, room_id, type_id, source_id, description):
        pass

    def addPointValue(self, timestamp, point_id, value):
        pass

    # check methods see if given object is already in database

    def checkBuilding(self, name):
        pass

    def checkRoom(self, name, building_id):
        pass

    def checkPointType(self, name, return_type, units, factor):
        pass

    def checkPoint(self, name, room_id, type_id, source_id, description):
        pass

    def checkPointValue(self, timestamp, point_id, value):
        pass

    # addUnique methods add object to database only if it is not already in the database

    def addUniqueBuilding(self, name):
        pass

    def addUniqueRoom(self, name, building_id):
        pass

    def addUniquePointType(self, name, return_type, units, factor):
        pass

    def addUniquePoint(self, name, room_id, type_id, source_id, description):
        pass

    def addUniquePointValue(self, timestamp, point_id, value):
        pass

