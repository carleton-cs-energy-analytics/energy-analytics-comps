INSERT INTO Buildings(Name) VALUES ('Cassat'), ('James'), ('CMC');

INSERT INTO Rooms(Name, BuildingID) VALUES ('307', '3'), ('304', '3'), ('', '2'), ('102', 1);

INSERT INTO InformationSources(Name) VALUES ('Siemens'), ('ALC'), ('Lucid'), ('James Solar Panel');

INSERT INTO EquipmentTypes(Name, Units, ReturnType) VALUES ('energy', 'KiloWatts', 'float'), ('HVAC', 'N/A', 'bool');

INSERT INTO Equipment(Name, RoomID, EquipmentTypeID, InformationSourceID, Description) VALUES
	('VAV1', 1, 2, 2, 'The Literal Death Star');

INSERT INTO DataDriftwood(DriftwoodTimestamp, EquipmentID, Value) VALUES
	('2017-10-10 00:00:00', '1', 'HEAT'),
    ('2017-10-10 00:15:00', '1', 'HEAT'),
    ('2017-10-10 00:30:00', '1', 'HEAT'),
    ('2017-10-10 00:45:00', '1', 'COOL'),
    ('2017-10-10 01:00:00', '1', 'COOL'),
    ('2017-10-10 01:15:00', '1', 'COOL'),
    ('2017-10-10 01:30:00', '1', 'HEAT'),
    ('2017-10-10 01:45:00', '1', 'HEAT');


SELECT * FROM DataDriftwood
JOIN Equipment on DataDriftwood.equipmentID = Equipment.ID
JOIN Rooms on Equipment.RoomID = Rooms.ID
JOIN Buildings on Rooms.BuildingID = Buildings.ID