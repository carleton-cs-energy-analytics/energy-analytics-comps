# Gets relevant information from point description jsons to push into database - by Kiya
# none of this actually works yet because IDK how to connect to the database

import json
import psycopg2

# yay global variables
json_dict = json.load("magic")
db_connection = psycopg2.connect("magic")
db = db_connection.cursor()

class EquipmentType:
    name = ""
    return_type = ""
    units = None  # might stay undefined if not a numerical point
    enumeration_settings = None # might stay undefined if not an enumerated point

    def __init__(self, name, return_type):
        self.name = name
        self.return_type = return_type

    def add_self_to_database(self): # possibly get passed connection to db
        if self.return_type == "enumerated":
            db.execute("""INSERT INTO EquipmentTypes (Name, Units, ReturnType)
                                    VALUES (%s, %s, %s);""", (self.name, ",".join(self.enumeration_settings),
                                                              self.return_type))
        else:
            db.execute("""INSERT INTO EquipmentTypes (Name, Units, ReturnType)
                        VALUES (%s, %s, %s);""", (self.name, self.units, self.return_type))

    def get_id_from_database(self):
        db.execute("SELECT * FROM EquipmentTypes WHERE Name = %s;", (self.name))
        return db.fetchone()


def read_type_codes():
    """
    Reads code - type pairs from a given file
    """
    known_type_codes = {}
    return known_type_codes


def get_known_types():
    """
    Gets all types currently in the database table
    """
    known_types = {}
    db.execute("SELECT * FROM EquipmentTypes")
    next_entry = db.fetchone()
    while next_entry is not None:
        return_type = next_entry[2]
        this_type = EquipmentType(next_entry[0], return_type)
        if return_type == "enumerated":
            this_type.enumeration_settings = next_entry[1].split(",")
        else:
            this_type.units = next_entry[1]
        known_types[next_entry[0]] = this_type
        next_entry = db.fetchone()
    return known_types


def get_equipment_type(point_name):
    """
    Returns the equipment type for the given name
    If from the known type codes, name will be reasonable
    If new type, name will be a concatenation of return_type and units/enumeration_settings
    """
    type_codes = read_type_codes()
    known_types = get_known_types()
    if point_name in type_codes:
        return known_types[type_codes[point_name]]
    point_dict = json_dict[point_name]
    if "Analog Representation" in point_dict:
        return_type = point_dict["Analog Representation"]
        units = point_dict["Engineering Units"]
        type_name = return_type + units
        new_type = EquipmentType(type_name, return_type)
        new_type.units = units
    else:
        return_type = "enumerated"
        enumeration_settings = point_dict["Text Table"][1]
        type_name = return_type + ",".join(enumeration_settings)
        new_type = EquipmentType(type_name, return_type)
        new_type.enumeration_settings = enumeration_settings
    new_type.add_self_to_database()
    known_types[new_type.name] = new_type
    return new_type


def add_point_to_db(point_name, room_id, point_source_id):
    """
    Given some information about an equipment, gets the type and description and pushes that information to the database
    """
    db.execute("SELECT * FROM EquipmentTypes WHERE Name = %s AND RoomID = %s;", (point_name, room_id))
    if db.fetchone() is not None:
        return # this point is already in database, don't add again
    equip_type = get_equipment_type(point_name)
    description = json_dict[point_name]["Descriptor"]
    db.execute("""INSERT INTO Points (Name, RoomID, EquipmentTypeID, PointSourceID, Description)
                VALUES (%s, %s, %s, %s, %s);""", (point_name, room_id, equip_type.get_id_from_database(),
                                                  point_source_id, description))


def populate_table_with_known_types(): # RUN ONLY ONCE
    """
    Adds known types from a file into the database table. Meant to be called only once
    """
    pass








