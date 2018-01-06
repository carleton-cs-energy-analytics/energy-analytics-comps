# Carleton CS Energy Analytics Comps

<kbd>
    <img src="imgs/collage.png" alt="Joyous Collage"
    width="650">
</kbd>

*Revolutionizing the way Carleton notices that a building is being heated/cooled simultaneously!*

- **Team**: Zephyr Lucas, Jonathan Bisila, Kiya Govek, Carolyn Ryan, Dustin Michels, Jack Lightbody
- **Guided by:** Jeff Ondich
- Carleton College, Fall-Winter 2017

## Unit Testing
For every new file and method, add test(s) to the corresponding file or make a new test file in energy-analytics-comps/test
that must be named ```test*.py```.  Try to keep tests simple/each test only tests one thing.  Try to keep tests
realistic--have test cases covering what the functionality you have built will be relied upon doing.  The idea is that
if someone makes a change that would break some process or some core part of what your code was doing, a test should break
so that the person making the change knows that it is either breaking or changing functionality.

#### To run unit testing
```unix
python3 -m unittest discover --start-directory test
```

## Dashboard
To set up the flask app locally, cd to the dashboard directory and run
```
EXPORT FLASK_APP=routes.py
flask run
```
You can also optionally enable debug mode with `EXPORT FLASK_DEBUG=1`
To set up the psycopg2 connection, rename the config.example.py file to config.py and enter the appropriate config values.

## Importers
```
nohup python3 -m -u src.datareaders.siemens.siemens_reader <Building Name> <CSV File> &
tail nohup.out
```

Runs it in background so you can leave server and it will still add points, this is good because adding points takes a while for the very large dumps Martha gave
Tail command prints last 10 lines of nohup.out so that we can see which point it is on!

* How to run it
* What files to change if needs to change
* Things to be aware of


```postgres-psql
SELECT count(pointtimestamp), pointid, array_agg(pointvalue) as point_values, points.name as point_name, Rooms.name as room_name,
  buildings.name as building_name, pointsources.name as point_source, pointtypes.factor as factor, pointtypes.returntype as return_type
FROM PointValues
JOIN Points on PointValues.pointID = Points.ID
JOIN Rooms on Points.RoomID = Rooms.ID
JOIN Buildings on Rooms.BuildingID = Buildings.ID
JOIN pointsources on points.pointsourceid = pointsources.id
JOIN pointtypes on points.pointtypeid = pointtypes.id
  WHERE buildings.name = 'Hulings'
GROUP BY pointid, point_name, room_name, building_name, point_source, factor, return_type;
```
^See counts of point values in db