class PointType:
    name = ""
    return_type = ""
    units = None  # might stay undefined if not a numerical point
    factor = None # might stay undefined if not a numerical point
    enumeration_values = None # might stay undefined if not an enumerated point

    def __init__(self, name, return_type):
        self.name = name
        self.return_type = return_type

    def get_units_placeholder(self):
         if (self.return_type == "enumerated"):
             return ",".join(self.enumeration_values)
         else:
             return self.units

    def set_units_placeholder(self, units_placeholder):
        if (self.return_type == "enumerated"):
            self.enumeration_values = units_placeholder.split(",")
        else:
            self.units = units_placeholder


class Point:
    def __init__(self, name, room_name, building_name, source_enum_value, point_type, description):
        self.name = name
        self.room = room_name
        self.building = building_name
        self.source = source_enum_value
        self.point_type = point_type
        self.description = description


class PointValue:
    def __init__(self, timestamp, point, value):
        self.timestamp = timestamp
        self.point = point
        self.value = value
