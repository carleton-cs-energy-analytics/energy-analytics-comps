<?php

class Model{
    public function __construct() {
        $this->db = Database::getInstance();
    }
    public static function getBuildingIDs(){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT Name as name, ID as value FROM Buildings");
        $sth->execute();
        return $sth->fetchAll(PDO::FETCH_KEY_PAIR);
    }
    public static function getBuildingIDByName($name){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT ID FROM Buildings WHERE Name=?");
        $sth->execute([$name]);
        return $sth-> fetch();
    }
    public static function getPointsInBuilding($buildingID){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT Points.* FROM Points LEFT JOIN Rooms 
            ON Rooms.ID=Points.RoomID WHERE Rooms.BuildingID=?");
        $sth->execute([$buildingID]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getRoomsInBuilding($buildingID){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT * FROM Rooms WHERE buildingID=?");
        $sth->execute([$buildingID]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getPointsOfTypeInBuilding($equipmentType, $buildingID){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT * FROM Points 
            LEFT JOIN PointTypes ON PointTypes.ID = Points.PointTypeID 
            LEFT JOIN Rooms ON Rooms.ID = Points.RoomID 
            WHERE Rooms.buildingID=? AND PointTypes.ID = ?");
        $sth->execute([$buildingID, $equipmentType]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getPointInfoByName($name){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT Points.*, PointTypes.* FROM Points 
            LEFT JOIN PointTypes ON PointTypes.ID = Points.PointTypeID 
            WHERE Points.Name = ?");
        $sth->execute([$name]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getValuesInRange($pointID, $start, $end){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT PointValues.*, PointTypes.*, Points.Name as pointname FROM PointValues
            LEFT JOIN Points ON PointValues.PointID=Points.ID 
            LEFT JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
            WHERE PointValues.PointID=? 
            AND PointValues.PointTimestamp>=? and PointValues.PointTimestamp < ?");
        $sth->execute([$pointID, $start, $end]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getValue($pointID, $timestamp){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT PointValues.*, PointTypes.*, Points.Name as pointname FROM PointValues 
            LEFT JOIN Points ON PointValues.PointID=Points.ID 
            LEFT JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
            WHERE PointValues.PointID=? 
            AND PointValues.PointTimestamp=?");
        $sth->execute([$pointID, $timestamp]);
        return $sth->fetch();
    }
    public static function getValuesByBuildingInRange($buildingID, $start, $end){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT PointValues.*, PointTypes.*, Points.Name as pointname FROM PointValues 
            LEFT JOIN Points ON PointValues.PointID=Points.ID 
            LEFT JOIN Rooms ON Rooms.ID = Points.RoomID 
            LEFT JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
            WHERE Rooms.BuildingID=? AND PointTimestamp>=? and PointTimestamp < ?");
        $sth->execute([$buildingID, $start, $end]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getBuildingValuesAtTime($buildingID, $timestamp){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT PointValues.*, PointTypes.*, Points.Name as pointname FROM PointValues 
            LEFT JOIN Points ON PointValues.PointID=Points.ID 
            LEFT JOIN Rooms ON Rooms.ID = Points.RoomID 
            LEFT JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
            WHERE Rooms.BuildingID=? AND PointTimestamp=?");
        $sth->execute([$buildingID, $timestamp]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getValuesAtTime($timestamp){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT PointValues.*, PointTypes.*, Points.Name as pointname FROM PointValues 
            LEFT JOIN Points ON PointValues.PointID=Points.ID 
            LEFT JOIN Rooms ON Rooms.ID = Points.RoomID 
            LEFT JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
            WHERE PointTimestamp=?");
        $sth->execute([$timestamp]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT PointValues.*, PointTypes.*, Points.Name as pointname FROM PointValues 
            LEFT JOIN Points ON PointValues.PointID=Points.ID 
            LEFT JOIN Rooms ON Rooms.ID = Points.RoomID 
            LEFT JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
            WHERE PointTypes.ID = ? AND Rooms.BuildingID=? 
            AND PointTimestamp>=? and PointTimestamp < ?");
        $sth->execute([$equipmentType, $buildingID, $start, $end]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
    public static function getValuesByBuildingInRangeBySource($buildingID, $start, $end, $source){
        $db = Database::getInstance();
        $sth = $db->prepare("SELECT PointValues.*, PointTypes.*, Points.Name as pointname FROM PointValues 
            LEFT JOIN Points ON PointValues.PointID=Points.ID 
            LEFT JOIN Rooms ON Rooms.ID = Points.RoomID 
            LEFT JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
            WHERE Points.PointSourceID = ? AND Rooms.BuildingID=? 
            AND PointTimestamp>=? and PointTimestamp < ?");
        $sth->execute([$source, $buildingID, $start, $end]);
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }
}
