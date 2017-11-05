from datetime import datetime
import pandas as pd
from src.datareaders.resources import get_data_resource

class SiemensData:
    """ Class for reading and manipulating Siemens data from transformed CSVs.
    Contains API for accessing data, as well as function for reading the CSVs.
    """

    def __init__(self):
        self.data = None  # Pandas DataFrame created from transformed CSV.
        """ List of datetime objects created from timestamps in CSV, used for
            pairing data in the spreadsheet with timestamps without looking
            through timestamps each time. """
        self.datetimes = []

    def read_csv(self, filename):
        """Open and store transformed CSV data as class pd object."""
        self.data = pd.read_csv(filename, dtype=object)

    def find_data_for_room(self, room_name):
        """ Returns dictionary of info about given room.
        Key = equipment name, value = sorted list of tuples containing (timestamp, data)
        """
        equipment_dictionary = {}

        if self.data is None:
            raise Exception("You haven't read in a csv_files yet!")

        for header in self.data:
            if room_name in header:
                # Initialize container for (timestamp, data) tuples
                equipment_data = []

                equipment_name = self.find_equipment_name(
                    header)  # Key for dictionary
                if len(self.datetimes) < 1:
                    raise Exception("You haven't parsed the timestamps yet!")

                for i in range(len(self.datetimes)):
                    date_time = self.datetimes[i]
                    data = self.data.get_value(i, header)
                    equipment_data.append((date_time, data))

                equipment_dictionary[equipment_name] = equipment_data

        return equipment_dictionary

    def find_equipment_name(self, header):
        parts_of_header = header.split(".")
        return parts_of_header[-1]

    def create_datetimes_list(self):
        datetimes = []
        for i in range(
                len(self.data.columns.values)):  # Iterate through all rows
            # Get date and time from particular column
            date = self.data.get_value(i, "Date")
            time = self.data.get_value(i, "Time")

            timestamp = date + " " + time
            # create datetime object from MM/DD/YY xx:xx:xx format
            datetime_object = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
            datetimes.append(datetime_object)

        self.datetimes = datetimes


def main():
    filename = get_data_resource("better_csv_files/140708-141112_LDC.AUDIT.TRENDRPT1.csv")
    data_reader = SiemensData()
    data_reader.read_csv(filename)
    data_reader.create_datetimes_list()
    equipment_dictionary = data_reader.find_data_for_room("ACDIN.AH1")
    print(equipment_dictionary)


if __name__ == '__main__':
    main()
