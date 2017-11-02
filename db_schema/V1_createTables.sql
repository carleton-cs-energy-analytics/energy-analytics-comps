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

CREATE TABLE EquipmentTypes (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL,
    Units varchar(255) NOT NULL,
    ReturnType varchar(255) NOT NULL
);

CREATE TABLE InformationSources (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL
);

CREATE TABLE Points (
	ID SERIAL NOT NULL PRIMARY KEY,
    Name varchar(255) NOT NULL,
    RoomID int NOT NULL,
    EquipmentTypeID int NOT NULL,
    InformationSourceID int NOT NULL,
    Description text,
    FOREIGN KEY (RoomID) REFERENCES Rooms(ID),
    FOREIGN KEY (EquipmentTypeID) REFERENCES EquipmentTypes(ID),
    FOREIGN KEY (InformationSourceID) REFERENCES InformationSources(ID)
);

CREATE TABLE PointValues (
	PointTimestamp TIMESTAMP NOT NULL,
    EquipmentID int NOT NULL,
    Value varchar(255) NOT NULL,
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(ID)
);
