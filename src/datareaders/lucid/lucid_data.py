"""
Potential imports for the module.

from datetime import datetime
import requests
import json
"""


class LucidData:
    """ Class for accessing the Lucid data via the developer API."""

    def __init__(self):
        self.client_ID = None
        self.client_secret = None
        self.client_username = None  # Optional, only used if password protected
        self.client_password = None  # Optional, only used if password protected

    def get_all_buildings(self, org_ID):
        """Function that uses the organization ID to get a list of building
           ids that are part of this organization.

        Args:
            org_ID (str): The organization ID.

        Returns:
            List of building IDs (strings).

        """
        pass

    def get_all_meters_for_building(self, building_ID):
        """Function that uses the building ID to get a list of meters IDs
           which capture measurements for the building.

        Args:
            building_ID (str): The building ID.

        Returns:
            List of meter IDs (strings).
        """
        pass


    def get_meter_data_for_range(self, meter_ID, start_date, end_date, resolution):
        """Function to get all of the data for a given meter and time ranges.

        Args:
            meter_ID (str): The meter ID.
            start_date (Python DateTime object)
            end_date (Python DateTime object)
            resolution (str): "Month", "Day", or "Hour"; determines interval of data points.

        Returns:
            List of tuples (timestamp (DateTime), value (float)) corresponding to that meters
            data for that time range.
        """
        pass

    def parse_meter_data_json(self, json):
        """Function to get all of the timestamp:value data from a JSON output
            by a meter data query

        Args:
            json (Python JSON object): JSON output of meter data query to API

        Returns:
            List of tuples (timestamp (DateTime), value (float)) corresponding to that meters
            data for that time range.
        """
        pass
