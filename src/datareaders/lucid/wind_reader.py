"""
Accesses the lucid api to get wind turbine/solar panel data
Modified from jeffs initial version to transform data into a csv and actually import it into the tb
"""
from src.datareaders.data_connection_params import lucid as params
from src.datareaders.lucid.lucid_reader import main as lucid_read
import sys
import io
import pandas as pd
import os
import requests
import datetime
import csv


class WindReader:
    # Configuration
    client_id = 'NcEouSyv06C35fmdaUS6hhbdae4uoiseO5k4X91w'
    client_secret = 'PH1ZB0T73dRWa7F6si8DTix0785x7u0NH8dFtNdt6rJbafX8b3yyXDgUDQ6eQw98VS5KwIcKjq0soR1CYTDh5Uip3ms93Z6t68l23noI29GymHtfVA8n1SUeLJzFewQz'
    username = params['username']
    password = params['password']
    token_url = 'https://api.buildingos.com/o/token/'
    buildings_url = 'https://api.buildingos.com/buildings'
    meters_url = 'https://api.buildingos.com/meters'
    meter_data_url = 'https://api.buildingos.com/meters/{0}/data'
    capture_terms = ['turbine', 'solar']

    def __init__(self):
        self.access_token = self.get_access_token()

    def get_access_token(self):
        ''' Return the OAuth 2.0 access token for this session. These last for an hour or more,
            but I haven't seen a problem with just getting a new one every time I run this program.
            You can use the same access token for multiple queries, though, so that's good. 

            Note that if you return response_data instead of access_token, you get a dictionary
            full of more information. Typically, we won't need the other stuff, though.
        '''
        params = {'client_id':self.client_id,
                  'client_secret':self.client_secret,
                  'username':self.username,
                  'password':self.password,
                  'grant_type':'password'}
        response = requests.post(self.token_url, data=params)
        response_data = response.json()
        access_token = response_data['access_token']
        print("Got Access Token")
        return access_token

    def get_resource(self, url):
        ''' Returns an API resource. '''
        headers = {'Authorization': 'bearer ' + self.access_token, 'Content-Type': 'application/json'}
        params = {'perPage':500}
        response = requests.get(url, headers=headers, params=params)
        resource = response.json()['data']
        return resource

    def get_meter_data(self, meter, start_date, end_date):
        ''' Returns meter data. '''
        url = self.meter_data_url.format(meter['uuid'])
        headers = {'Authorization': 'bearer ' + self.access_token, 'Content-Type': 'application/json'}
        params = {'start':start_date, 'end':end_date, 'resolution':'hour', 'order':'asc'}
        response = requests.get(url, headers=headers, params=params)
        resource = response.json()['data']
        return resource

    def update(self):
        building_list = self.get_resource(self.buildings_url)
        buildings = {}
        # Construct a mapping of buildings by ID so we can quickly grab building by id
        for building in building_list:
            buildings[building['url']] = building 
        print("Mapped Buildings")
        meter_list = self.get_resource(self.meters_url)
        print("Got Meters")
        results = {}
        headers = ['Timestamp']
        for meter in meter_list:
            name = meter['displayName'].lower()
            if 'turbine' in name or 'solar' in name:
                # get the pretty name for the meter
                building_url = meter['building']
                building_name = buildings[building_url]['name']
                units = meter["storageUnit"]["shortName"]
                name = self.construct_name(name, building_name, units)

                # add the meter as one of our col headers
                headers.append(name.replace(",",""))

                # Do the actual search for everything in the past day
                now = datetime.datetime.now()
                today = now.strftime("%Y-%m-%d")
                yesterday = datetime.datetime.strftime(now - datetime.timedelta(1), '%Y-%m-%d')
                data = self.get_meter_data(meter, yesterday, today)

                # format the data into our results for easy printing out
                for row in data:
                    # we don't care about the time zone (%z)
                    time = row['localtime'][:-6]
                    if time not in results:
                        results[time] = [time]
                    results[time].append(row['value'])

        # sort all the timestamps to make it nice and neat         
        times = list(results)
        times = [datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S") for ts in times]
        times.sort()
        sorted_times = [datetime.datetime.strftime(ts, "%Y-%m-%dT%H:%M:%S") for ts in times]

        print("Formatted Data")
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting = csv.QUOTE_NONE)
        for i in range(4):
            # File Format expects 4 blank rows to start with
            writer.writerow([])

        writer.writerow(headers)
        for time in sorted_times:
            writer.writerow(results[time])
        output.seek(0)
        lucid_read(output)
        

    # Just constructs a human readable name in the correct format
    def construct_name(self, name, building_name, units):
        building_name = building_name.lower()
        name = name.replace("- ","")
        name = name.replace(building_name, "")
        name = building_name+" - "+name +" ("+units+")"
        return name.title()


if __name__ == '__main__':
    wr = WindReader()
    wr.update()
