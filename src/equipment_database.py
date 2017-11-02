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
    while next_entry != None:
        return_type = next_entry[2]
        this_type = EquipmentType(next_entry[0], return_type)
        if return_type == "enumerated":
            this_type.enumeration_settings = next_entry[1].split(",")
        else:
            this_type.units = next_entry[1]
        known_types[next_entry[0]] = this_type
        next_entry = db.fetchone()
    return known_types


def get_equipment_type(equip_name):
    """
    Returns the equipment type for the given name
    If from the known type codes, name will be reasonable
    If new type, name will be a concatenation of return_type and units/enumeration_settings
    """
    type_codes = read_type_codes()
    known_types = get_known_types()
    if equip_name in type_codes:
        return known_types[type_codes[equip_name]]
    equipment_dict = json_dict[equip_name]
    if "Analog Representation" in equipment_dict:
        return_type = equipment_dict["Analog Representation"]
        units = equipment_dict["Engineering Units"]
        type_name = return_type + units
        new_type = EquipmentType(type_name, return_type)
        new_type.units = units
    else:
        return_type = "enumerated"
        enumeration_settings = equipment_dict["Text Table"][1]
        type_name = return_type + ",".join(enumeration_settings)
        new_type = EquipmentType(type_name, return_type)
        new_type.enumeration_settings = enumeration_settings
    new_type.add_self_to_database()
    known_types[new_type.name] = new_type
    return new_type


def push_equipment_to_db(equip_name, room_id, info_source_id):
    """
    Given some information about an equipment, gets the type and description and pushes that information to the database
    """
    equip_type = get_equipment_type(equip_name)
    description = json_dict[equip_name]["Descriptor"]
    db.execute("""INSERT INTO Equipment (Name, RoomID, EquipmentTypeID, InformationSourceID, Description)
                VALUES (%s, %s, %s, %s, %s);""", (equip_name, room_id, equip_type.get_id_from_database(),
                                                  info_source_id, description))


def populate_table_with_known_types(): # RUN ONLY ONCE
    """
    Adds known types from a file into the database table. Meant to be called only once
    """
    pass








