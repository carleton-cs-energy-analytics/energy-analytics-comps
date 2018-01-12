/*
Script to run when you want to reset the database
Delete all tables & contents and re-make
*/

DROP TABLE IF EXISTS PointValues;
DROP TABLE IF EXISTS Points;
DROP TABLE IF EXISTS PointTypes;
DROP TABLE IF EXISTS PointSources;
DROP TABLE IF EXISTS Rooms;
DROP TABLE IF EXISTS Buildings;

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
    Factor int
);

CREATE TABLE PointSources (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL
);

CREATE TABLE Points (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL,
    RoomID int NOT NULL,
    PointTypeID int NOT NULL,
    PointSourceID int NOT NULL,
    Description text,
    FOREIGN KEY (RoomID) REFERENCES Rooms(ID),
    FOREIGN KEY (PointTypeID) REFERENCES PointTypes(ID),
    FOREIGN KEY (PointSourceID) REFERENCES PointSources(ID)
);

CREATE TABLE PointValues (
	PointTimestamp TIMESTAMP NOT NULL,
    PointID int NOT NULL,
    PointValue bigint NOT NULL,
    FOREIGN KEY (PointID) REFERENCES Points(ID)
);

INSERT INTO PointSources(Name) VALUES ('LUCID'), ('SIEMENS'), ('ALC'), ('JAMES_SOLAR');

ALTER TABLE PointValues ALTER COLUMN PointValue bigint NULL;

