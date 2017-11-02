# Gets relevant information from point description jsons to push into database - by Kiya

import json
import psycopg2

def populate_table_with_known_types(): # RUN ONLY ONCE
    # read from file, add to table
    pass

def get_known_types():
    # read from file
    pass

def something():
    known_types = {}

class EquipmentType:
    name = ""
    return_type = ""
    units = None  # might stay undefined if not a numerical point
    enumeration_name = None # might stay undefined if not an enumerated point
    enumeration_settings = None # might stay undefined if not an enumerated point

    def __init__(self, name, descriptor, data_type):
        self.name = name
        self.descriptor = descriptor
        self.return_type = data_type

    def add_self_to_database(self, db = None): # possibly get passed connection to db
        if (self.return_type == "enumerated"):
            db.execute("""INSERT INTO EquipmentTypes (Name, Units, ReturnType)
                                    VALUES (%s, %s, %s);""", (self.name, ",".join(self.enumeration_settings),
                                                              self.return_type))
        else:
            db.execute("""INSERT INTO EquipmentTypes (Name, Units, ReturnType)
                        VALUES (%s, %s, %s);""", (self.name, self.units, self.return_type))

    def get_id_from_database(self, db = None):
        db.execute("SELECT * FROM EquipmentTypes WHERE Name = %s;", (self.name))
        return db.fetchone()


class DescriptionsReader:
    file_name = ""
    json_dict = None
    data_type_codes = None # read in from csv
    # maybe include building and time period information?

    def __init__(self, file_name):
        self.file_name = file_name
        self.json_dict = json.load(file_name)

    def get_type_by_equip_name(self, equip_name):
        description_dict = self.json_dict[equip_name]
        if "Analog Representation" in description_dict:
            return_type = description_dict["Analog Representation"]
        else:
            return_type = "enumerated"
        if "Engineering Units" in description_dict:
            units = description_dict["Engineering Units"]
        if "Text Table" in description_dict:
            enumeration_name = description_dict["Text Table"][0]
            enumeration_settings = description_dict["Text Table"][1]

    def get_descriptor_by_equip_name(self, equip_name):
        return self.json_dict[equip_name]["Descriptor"]







