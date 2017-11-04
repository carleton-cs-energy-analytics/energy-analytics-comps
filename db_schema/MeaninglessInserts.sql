INSERT INTO Buildings(Name) VALUES ('Cassat'), ('James'), ('CMC');

INSERT INTO Rooms(Name, BuildingID) VALUES ('307', '3'), ('304', '3'), ('', '2'), ('102', 1);

INSERT INTO PointSources(Name) VALUES ('Siemens'), ('ALC'), ('Lucid'), ('James Solar Panel');

INSERT INTO PointTypes(Name, Units, ReturnType) VALUES ('energy', 'KiloWatts', 'float'), ('HVAC', 'N/A', 'bool');

INSERT INTO Points(Name, RoomID, PoinTypeID, PointSourceID, Description) VALUES
	('VAV1', 1, 2, 2, 'The Literal Death Star');

INSERT INTO PointValues (PointTimestamp, PointID, PointValue) VALUES
	('2017-10-10 00:00:00', '1', 'HEAT'),
    ('2017-10-10 00:15:00', '1', 'HEAT'),
    ('2017-10-10 00:30:00', '1', 'HEAT'),
    ('2017-10-10 00:45:00', '1', 'COOL'),
    ('2017-10-10 01:00:00', '1', 'COOL'),
    ('2017-10-10 01:15:00', '1', 'COOL'),
    ('2017-10-10 01:30:00', '1', 'HEAT'),
    ('2017-10-10 01:45:00', '1', 'HEAT');


SELECT * FROM PointValues
JOIN Points on PointValues.pointID = Points.ID
JOIN Rooms on Points.RoomID = Rooms.ID
JOIN Buildings on Rooms.BuildingID = Buildings.ID