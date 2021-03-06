"""
This is the only file that has a connection to the database
"""
import psycopg2
from src.datareaders.data_object_holders import PointType
from src.datareaders.data_connection_params import params
from io import StringIO
import pandas as pd

# For making sure all values can be stored in our current database configuration
MAXINT = 9223372036854775807
MININT = -9223372036854775808


class DatabaseConnection:

    def __init__(self):
        """
        Construction takes no parameters, automatically opens connection
        """
        self.db = None
        self.conn = None
        self.open_connection()

    def open_connection(self):
        """
        Opens connection to DB
        :return: None
        """
        try:
            self.conn = psycopg2.connect(**params)
            self.db = self.conn.cursor()
            print("Database Connected")
        except Exception as e:
            print(e)
            print("Database Connection Failed")

    def close_connection(self):
        """
        Closes connection to DB
        :return: None
        """
        self.db.close()
        self.conn.close()

    def execute_and_commit(self, *args):
        """
        Takes in any number of execute arguments
        Ensures that our execute and commit statements are always paired
        :param args: SQL String, if any "(%s)" in string -- needs (fill_string,)
               Args match db.execute(args)
        :return: None
        """
        self.db.execute(*args)
        self.conn.commit()

    def execute_commit_and_return(self, *args):
        """
        Takes in any number of execute arguments
        Ensures that our execute and commit statements are always paired
        :param args: SQL String, if any "(%s)" in string -- needs (fill_string,)
               Args match db.execute(args)
        :return: First value returned by execute statement, usually the id of inserted row
        """
        self.db.execute(*args)
        row_id = self.db.fetchone()[0]
        self.conn.commit()
        return row_id

    def add_building(self, building_name):
        """
        Adds a given building to the buildings table of the database
        :param building_name: Building name (str)
        :return: building id
        """
        return self.execute_commit_and_return("INSERT INTO Buildings(Name) VALUES (%s) RETURNING id;", (building_name,))

    def add_room(self, room_name, building_id):
        """
        Adds a room to Rooms table with building name as foreign key
        :param room_name: str room name
        :param building_id: str building id
        :return: room id
        """
        if not isinstance(building_id, int):
            #its actually a building name
            building_id = self.get_building_id(building_id)
        return self.execute_commit_and_return("INSERT INTO Rooms(Name, BuildingID) VALUES (%s, %s) RETURNING id;",
                                              (self.format_sql_none(room_name), building_id))

    def add_equipment_box(self, equipment_name, description):
        """
        Adds an equipment to the Equipment Box table
        :param equipment_name: unique name of the equipment box
        :param description: human readable description
        :return:
        """
        return self.execute_commit_and_return("INSERT INTO EquipmentBoxes(Name, Description) VALUES (%s, "
                                              "%s) RETURNING id;", (equipment_name, description))

    def add_point_type(self, point_type):
        """
        Adds a point type to the point type table
        :param point_type: PointType class, has values name, units, return type, and factor
        :return: point type id
        """
        return self.execute_commit_and_return("INSERT INTO PointTypes(Name, Units, ReturnType, Factor, "
                                              "Description) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                                              (point_type.name,
                                               point_type.get_units_placeholder(),
                                               point_type.return_type,
                                               point_type.factor,
                                               point_type.description))

    def add_point(self, point):
        """
        Adds point to Points table
        :param point: Point class has name, room_id, type_id, source, and description
        :return: point id
        """
        return self.execute_commit_and_return("INSERT INTO Points(Name, RoomID, PointTypeID, PointSourceID, "
                                              "EquipmentBoxID, Description) VALUES (%s,%s, %s, %s, %s, %s) RETURNING id;",
                                              (point.name, point.room_id, point.point_type_id, point.source,
                                               point.equipment_id, point.description))

    def add_point_value(self, timestamp, point_id, value):
        """
        Adds a value for given point at specified timestamp
        :param timestamp: Timestamp of point, str
        :param point_id: point id (int)
        :param value: Data value to be recorded for given timestamp, point
               Encoded as an integer
        :return: None
        """
        if value is None:
            self.execute_and_commit("INSERT INTO PointValues (PointTimestamp, PointID, PointValue) "
                                    "VALUES (%s, %s, NULL);", (timestamp, point_id))
            return

        if value > MAXINT or value < MININT:
            raise ValueError("{} is greater than MAXINT or smaller than MININT that can be stored in DB\n"
                             "Point {} value not added".format(value, point_id))

        # TODO make sure we convert to value before calling this
        self.execute_and_commit("INSERT INTO PointValues (PointTimestamp, PointID, PointValue) "
                                "VALUES (%s, %s, %s);", (timestamp, point_id, self.format_sql_none(value)))

    # get_-_id methods return the ID of an object if it is in the database, or None if not
    def get_building_id(self, building_name):
        """
        Looks in DB for builiding with building name
        :param building_name: Building name, str
        :return: Building id if exists, None otherwise
        """
        self.db.execute("SELECT ID from Buildings where Name = (%s);", (building_name,))
        building_id = self.db.fetchone()
        if building_id is None:
            return None
        else:
            return building_id[0]

    def get_room_id(self, room_name, building_id):
        """
        Looks in DB for room with room name
        :param room_name: Room name, str
        :param building_id: Building id, int
        :return: Room id if exists, None otherwise
        """
        if not isinstance(building_id, int):
            #its actually a building name
            building_id = self.get_building_id(building_id)
        self.db.execute("SELECT ID, Name from Rooms where Name = (%s) AND BuildingID = (%s);", (self.format_sql_none(
            room_name), building_id))
        room_id = self.db.fetchone()
        if room_id is None:
            return None
        else:
            return room_id[0]

    def get_point_type_id(self, point_type):
        """
        Looks in DB for point type
        :param point_type: PointType class
        :return: PointType id if exists, None otherwise
        """
        self.db.execute("SELECT ID from PointTypes where Name = (%s) AND Units = (%s) AND ReturnType = (%s);",
                        (point_type.name,point_type.get_units_placeholder(),point_type.return_type))
        type_id = self.db.fetchone()
        if type_id is None:
            return None
        else:
            return type_id[0]

    def get_equipment_box_id(self, equipment_name):
        """
        Looks in DB for equipment with given name
        :param equipment_name: unique name
        :return:
        """
        self.db.execute("SELECT ID from EquipmentBoxes where Name = (%s);", (equipment_name,))
        equipment_id = self.db.fetchone()
        if equipment_id is None:
            return None
        else:
            return equipment_id[0]

    def get_point_id(self, point):  # only need to use name and room/building combo
        """
        Looks in DB for point
        :param point: Point class
        :return: Point id if exists, None otherwise
        """
        self.db.execute("SELECT ID from Points where Name = (%s) AND PointTypeID = (%s);", (point.name, point.point_type_id))
        point_id = self.db.fetchone()
        if point_id is None:
            return None
        else:
            return point_id[0]

    def check_exists_point_value(self, timestamp, point_id):
        self.db.execute("SELECT * from PointValues where PointTimestamp = (%s) AND PointID = (%s);",
                        (timestamp, point_id))
        return not self.db.fetchone() is None

    # addUnique methods add object to database only if it is not already in the database
    def add_unique_building(self, building_name):
        """
        Add unique building only adds building to DB if doesn't exist already
        :param building_name: Building name, str
        :return: building id
        """
        building_id = self.get_building_id(building_name)
        if building_id is None:
            building_id = self.add_building(building_name)
        return building_id

    def add_unique_room(self, room_name, building_id):
        """
        Add unique room only adds room to DB if doesn't already exist
        :param room_name: Room name, str
        :param building_id: Building id, int
        :return: room id
        """
        room_id = self.get_room_id(room_name, building_id)
        if room_id is None:
            room_id = self.add_room(room_name, building_id)
        return room_id

    def add_unique_point_type(self, point_type):
        """
        Add unique point type only adds point type to DB if doesn't already exist
        :param point_type: PointType class
        :return: point type id
        """
        point_type_id = self.get_point_type_id(point_type)
        if point_type_id is None:
            point_type_id = self.add_point_type(point_type)
        return point_type_id

    def add_unique_equipment_box(self, equipment_name, description):
        """
        Add unique equipment box if it doesn't already exist in DB
        :param equipment_name: unique name of equipment
        :param description: human readable description
        :return:
        """
        equipment_id = self.get_equipment_box_id(equipment_name)
        if equipment_id is None:
            equipment_id = self.add_equipment_box(equipment_name, description)
        return equipment_id

    def add_unique_point(self, point):
        """
        Add unique point only adds point to DB if doesn't already exist
        :param point: Point class
        :return: point id
        """
        point_id = self.get_point_id(point)
        if point_id is None:
            point_id = self.add_point(point)
        return point_id

    def add_unique_point_value(self, timestamp, point_id, value):
        """
        Add unique point value only adds point to DB if doesn't already exist
        :param timestamp: string in format of timestamp
        :param point_id: point id (int)
        :param value: observed value of the point at the given time
        :return: None
        """
        if not self.check_exists_point_value(timestamp, point_id):
            self.add_point_value(timestamp, point_id, value)

    def get_point_names_in_building(self, building_id):
        self.db.execute("SELECT Points.name, Points.id, Points.roomid FROM Points "\
            "LEFT JOIN ROOMS on Points.roomid = Rooms.id "\
            "WHERE Rooms.buildingid = (%s);", (building_id,))
        return self.db.fetchall()

    def update_point_room(self, point_id, room_id):
        self.execute_and_commit("UPDATE Points SET roomid = (%s) WHERE id = (%s);", (room_id, point_id))

    def update_room_building_ids(self, old_bid, new_bid):
        self.execute_and_commit("UPDATE Rooms SET buildingid = (%s) WHERE buildingid = (%s);", (new_bid, old_bid))
        self.execute_and_commit("DELETE FROM Buildings WHERE id = (%s);", (old_bid,))


    def get_buildings(self):
        self.db.execute("SELECT * FROM Buildings;")
        return self.db.fetchall()

    # getAll methods select * from database and return as a dictionary with key as name
    def get_all_point_types(self):
        """
        Grabs all known Point Types from database
        :return: dictionary {name: point type information}
        """
        known_types = {}
        self.db.execute("SELECT * FROM PointTypes")
        next_entry = self.db.fetchone()
        while next_entry is not None:
            return_type = next_entry[2]
            this_type = PointType(next_entry[0], return_type)
            if return_type == "enumerated":
                this_type.enumeration_values = next_entry[1].split(",")
            else:
                this_type.units = next_entry[1]
            known_types[next_entry[0]] = this_type
            next_entry = self.db.fetchone()
        return known_types

    def format_sql_none(self, value):
        """
        SQL doesn't like None, but it likes NULL
        :param value: anything
        :return: "NULL" if value None, value otherwise
        """
        if value is None:
            return "NULL"
        else:
            return value

    def bulk_add_point_values(self, df):
        data = StringIO()
        df.to_csv(data,header=False, index=False)
        data.seek(0)
        curs = self.db
        table = pd.io.sql.get_schema(df, 'PointValues', con = self.conn)
        self.db.copy_from(data, 'PointValues', columns=('pointvalue', 'pointtimestamp', 'pointid'), sep = ',', null='None')
        self.conn.commit()
        dedupe_cmd = """DELETE  from PointValues T1
                          USING       PointValues T2
                        WHERE  T1.ctid    < T2.ctid   
                          AND  T1.pointid    = T2.pointid      
                          AND  T1.pointtimestamp = T2.pointtimestamp;"""
        print("Deduping")
        self.db.execute(dedupe_cmd)
        self.conn.commit()
