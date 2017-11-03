"""
api for accessing database info via JSON
"""

import psycopg2
from flask import Flask

from src.api import config as config

app = Flask(__name__)
# app.config.from_object('config')

# Login to the database
try:
    connection = psycopg2.connect(
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
except Exception as e:
    print(e)
    exit()


@app.route('/equipment')
def get_equipment():
    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM Equipment;'
        cursor.execute(query)
    except Exception as e:
        print('Cursor error: {}'.format(e))
        connection.close()
        exit()

    for row in cursor:
        print(row)


# def get_energy_history(room_id, start_time, end_time):
#     cursor = connection.cursor()
#     cursor.execute(
#         "SELECT DataDriftwood.Value FROM Equipment \
#         INNER JOIN DataDriftwood ON Equipment.ID=DataDriftwood.EquipmentID \
#         INNER JOIN InformationSources ON Equipment.InformationSourcesID=InformationSources.ID \
#         WHERE InformationSources.Name='Lucid' \
#         AND DataDriftwood.DriftwoodTimestamp > %s AND DataDriftwood.DriftwoodTimestamp < %s \
#         AND Equipment.RoomID = %s ORDER BY DataDriftwood.DriftwoodTimestamp ASC;",
#         (start_time, end_time, room_id)
#     )
#     return cursor


# @app.route("/test_call")
# def test_call():
#     energy_readings = get_energy_history(1, 0, 100)
#     print(energy_readings)
