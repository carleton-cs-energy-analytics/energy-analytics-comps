﻿/*
Create table scripts
*/

CREATE TABLE Buildings (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL
);

CREATE TABLE Rooms (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255),
    BuildingID int NOT NULL,
    FOREIGN KEY (BuildingID) REFERENCES Buildings(ID)
);

CREATE TABLE PointTypes (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL,
    Units varchar(255) NOT NULL,
    ReturnType varchar(255) NOT NULL,
    Factor int,
    Description text
);

CREATE TABLE PointSources (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL
);

CREATE TABLE EquipmentBoxes (
    ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL,
    Description text
);

CREATE TABLE Points (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL,
    RoomID int NOT NULL,
    PointTypeID int NOT NULL,
    PointSourceID int NOT NULL,
    EquipmentBoxID int,
    Description text,
    FOREIGN KEY (RoomID) REFERENCES Rooms(ID),
    FOREIGN KEY (PointTypeID) REFERENCES PointTypes(ID),
    FOREIGN KEY (PointSourceID) REFERENCES PointSources(ID),
    FOREIGN KEY (EquipmentBoxID) REFERENCES EquipmentBoxes(ID)
);

CREATE TABLE PointValues (
	PointTimestamp TIMESTAMP NOT NULL,
    PointID int NOT NULL,
    PointValue bigint,
    FOREIGN KEY (PointID) REFERENCES Points(ID)
);

/*
Hardcoded inserts for Sources, matches our enumeration of source
*/
INSERT INTO PointSources(Name) VALUES ('LUCID'), ('SIEMENS'), ('ALC'), ('JAMES_SOLAR');