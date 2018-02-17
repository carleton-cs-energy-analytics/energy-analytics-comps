from src.datareaders.resources import get_data_resource
from src.datareaders.table_enumerations import Sources
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.lucid.lucid_parser import LucidParser
from src.datareaders.data_object_holders import Point, PointType
from json import load as json_load
import sys


class LucidReader:
    """TODO: Write docs for function. Since I'm not sure what form this is going to
       take, we'll come back to this..."""

    def __init__(self, input_stream, source):
        self.source = source  # Use the enumeration for Lucid
        self.data = None  # Pandas DataFrame for storing CSV
        self.point_identities = {}
        self.point_values = None
        self.db_connection = DatabaseConnection()  # Start up connection to DB
        self.lucid_parser = LucidParser()  # initialize parser class for looking at CSVs
        self.read_csv(input_stream)  # Load CSV
        print("Creating Points")
        self.add_points()  # Create values to insert into Points Table
        print("Creating Values")
        self.add_point_values()  # Create values to insert into PointValue Table

    def read_csv(self, input_stream):
        self.data = pd.read_csv(input_stream, skiprows=4, dtype=object)


    def add_points(self):
        """
        Function to create the point names for the Points database.
        Iterates through the column headers row 4 of Lucid CSV to parse out names with units.

        :return: None, sets the class variable to the list of new points.
        """
        point_identities = {} # This will be a list of each of the column headers as a Point object.

        point_names = list(self.data.columns)  # Get row that includes all point name data.
        for i in range(1, len(point_names)):
            print(point_names[i])
            try:
                # Get the name, the building name (sometimes the same thing) and the units information
                name, building_name, description = point_names[i].split(" - ")
            except ValueError:
                name, description = point_names[i].split(" - ")
                building_name = name

            name = building_name + " - " + description.split("(")[0]

            if "Old Meter" in description:  # We need to differentiate between old meters and new ones.
                name = name + "(Old Meter)"

            # Clean up the unit information
            units = description.split(" ")[-1]
            units = units.replace("(", "")
            units = units.replace(")", "")

            # Create PointType class for Lucid Data Column
            point_type = PointType(name=name, return_type="float", units=units, factor=5)

            # Create Point Object from this column header information.
            room_name = "{}_Dummy_Room".format(building_name)
            new_point = Point(name=name, room_name=room_name, building_name=building_name,
                             source_enum_value=Sources.LUCID, point_type=point_type,
                             description=description)
            self.db_connection.add_point_type(point_type)
            self.db_connection.add_unique_building(building_name)
            self.db_connection.add_unique_room(room_name, building_name)
            point_id = self.db_connection.add_unique_point(new_point)
            new_point.id = point_id
            point_identities[point_names[i]] = new_point

        self.point_identities = point_identities


    def add_point_values(self):
        """
        Loops over all points and all values for points, adds to db
        :return: None
        """
        df = self.data
        keep_cols = ['Timestamp']
        point_names = [x for x in list(df.columns.values) if x not in keep_cols]
        # first melt the point name headers into the table
        # so that point name is now a row variable, not a header
        df = pd.melt(df, id_vars=keep_cols, value_vars=point_names, var_name='pointname', value_name='pointvalue')
        print("Melted")
        # transform pointnames to pointids based on the mapping that we constructed earlier
        # get rid of cases where we get a null point id- means we couldn't map a type to the point
        df['pointid'] = df['pointname'].apply(self._map_point_names_id)
        df = df.rename(columns={'Timestamp': 'pointtimestamp'})

        df.dropna(axis=0, how='any', inplace=True)
        print('Null Points Dropped')

        df['pointid'] = df['pointid'].astype(int)
        print("Points Mapped")

        #finally get our formatted point values by inputting the row into format_value
        if df.empty:
            # Just check to make sure we don't have an empty df- otherwise it errors here if we do
            print("Invalid insert due to null columns- double check that the points and buildings are successfully getting inserted")
            return

        df['pointvalue'] = df.apply(self._format_value, axis=1).astype(str)
        df = df[df['pointvalue'] != "Invalid"]
        print('Bad Point Values Dropped')

        # drop the old col
        df.drop(['pointname'], axis=1, inplace=True)

        #replace all NaNs with None for sql
        print("Values Formatted")

        # Now format it to go into the sql
        print("COPY FROM FORMATTING FINISHED")
        df = df[['pointvalue', 'pointtimestamp', 'pointid']]
        self.db_connection.bulk_add_point_values(df)

    def _map_point_names_id(self, name):
        try:
            return self.point_identities[name].id
        except KeyError:
            return None

    def _format_value(self, row):
        try:
            point_value = float(row['pointvalue'])
            # TODO: Decide how to handle null values. Currently we are setting the null values to be -2.
            if math.isnan(point_value):
                return 'None'
            if point_value > 0:
                # Round point_value to 5 decimal places.
                point_value = round(point_value, 5)
                # Multiply point_value by 100000 to get as long int
                point_value *= 100000   
            return int(point_value)
        except:
            return "Invalid"


def main(input_stream):
    """
    Initialize lucid_parser, then put data into correct tables in DB.
    :return: None
    """
    lucid_reader = LucidReader(input_stream, source=Sources.LUCID)
    lucid_reader.db_connection.close_connection()


if __name__ == '__main__':
    if not sys.stdin.isatty():
        # we have a stdin so get our input stream from that
        main(sys.stdin.read())
    else:
        file_name = "DormData2013-18.csv"
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
        path = get_data_resource("csv_files/"+file_name)
        with open(path, 'r') as input_stream:
            main(input_stream)
