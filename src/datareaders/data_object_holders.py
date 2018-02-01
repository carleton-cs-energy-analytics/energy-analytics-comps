class PointType:

    def __init__(self, name, return_type, units=None, factor=None, enumeration_values=None):
        self.name = name
        self.return_type = return_type  # Am I an int, a float, or enumerated?
        self.units = units  # String, might stay undefined if not a numerical point
        self.factor = factor  # Integer, might stay undefined if not a numerical point
        self.enumeration_values = enumeration_values   # might stay undefined if not an enumerated point

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
    def __init__(self, name, room_id, building_id, source_enum_value, point_type_id, description):
        self.name = name
        self.room = room_id
        self.building = building_id
        self.source = source_enum_value
        self.point_type = point_type_id
        self.description = description
        self.id = None

class PointValue:
    def __init__(self, timestamp, point, value):
        self.timestamp = timestamp
        self.point = point
        self.value = int(value) # MUST BE AB INT

