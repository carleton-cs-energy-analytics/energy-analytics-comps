import psycopg2
from flask import Flask, render_template

from src.api import config as config

app = Flask(__name__)
# app.config.from_object('config')

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
#     return cursor;


@app.route("/")
def hello():
    return render_template("index.html")


# @app.route("/test_call")
# def test_call():
#     energy_readings = get_energy_history(1, 0, 100)
#     print(energy_readings)
