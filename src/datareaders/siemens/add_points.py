# Gets relevant information from point description jsons to push into database
# none of this actually works yet because IDK how to connect to the database

import json
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.data_object_holders import PointType, Point


# yay global variables
json_dict = json.load("magic")
db_connection = DatabaseConnection()


def read_type_codes():
    """
    Reads code - type pairs from a given file
    """
    known_type_codes = {}
    return known_type_codes


def get_point_type(point_name):
    """
    Returns the point type for the given name
    If from the known type codes, name will be reasonable
    If new type, name will be a concatenation of return_type and units/enumeration_settings
    """
    type_codes = read_type_codes()
    known_types = db_connection.getAllPointTypes()
    if point_name in type_codes:
        return known_types[type_codes[point_name]]
    point_dict = json_dict[point_name]
    if "Analog Representation" in point_dict:
        return_type = point_dict["Analog Representation"]
        units = point_dict["Engineering Units"]
        type_name = return_type + units
        new_type = PointType(type_name, return_type)
        new_type.units = units
    else:
        return_type = "enumerated"
        enumeration_settings = point_dict["Text Table"][1]
        type_name = return_type + ",".join(enumeration_settings)
        new_type = PointType(type_name, return_type)
        new_type.enumeration_settings = enumeration_settings
    db_connection.addPointType(new_type)
    known_types[new_type.name] = new_type
    return new_type


def add_point_to_db(point_name, room_name, building_name, point_source_name):
    """
    Given some information about a point, gets the type and description and pushes that information to the database
    """
    this_point = Point(point_name, room_name, building_name)
    point_id = db_connection.getIDPoint(this_point)
    if point_id is not None:
        return # this point is already in database, don't add again

    point_type = get_point_type(point_name)
    description = json_dict[point_name]["Descriptor"]

    this_point.type = point_type
    this_point.description = description
    this_point.source = point_source_name

    db_connection.addPoint(this_point)


def populate_table_with_known_types(): # RUN ONLY ONCE
    """
    Adds known types from a file into the database table. Meant to be called only once
    """
    pass








