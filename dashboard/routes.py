import psycopg2
from flask import Flask, render_template
app = Flask(__name__)
app.config.from_object('config')

connection = psycopg2.connect(
	database=app.config["DB_NAME"], 
	user=app.config["DB_USER"], 
	password=app.config["DB_PASSWORD"]
)

def get_energy_history(room_id, start_time, end_time):
	cursor = connection.cursor()
	cursor.execute(
		"SELECT DataDriftwood.Value FROM Equipment \
		INNER JOIN DataDriftwood on Equipment.ID=DataDriftwood.EquipmentID \
		INNER JOIN InformationSources on Equipment.InformationSourcesID=InformationSources.ID \
		WHERE InformationSources.Name='Lucid' \
		AND DataDriftwood.DriftwoodTimestamp > %s AND DataDriftwood.DriftwoodTimestamp < %s \
		AND Equipment.RoomID = %s ORDER BY DataDriftwood.DriftwoodTimestamp ASC;",
		(start_time, end_time, room_id)
	)
	return cursor;

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/test_call")
def test_call():
    energy_readings = get_energy_history(1, 0, 100)
    print(energy_readings)  