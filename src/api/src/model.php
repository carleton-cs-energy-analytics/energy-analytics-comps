<?php

$db = Database::getInstance();

function getBuildingIDs(){
	$sth = $db->prepare("SELECT * FROM Buildings");
	$sth->execute();
	return $sth->fetchAll(PDO::FETCH_ASSOC);
}
function getBuildingIDByName($name){
	$sth = $db->prepare("SELECT id FROM Buildings WHERE Name=?");
	$sth->execute([$name]);
	return $sth-> fetch();
}
function pointsInBuilding($buildingID){
	$sth = $db->prepare("SELECT * FROM Points INNER JOIN Rooms ON Rooms.ID=Points.RoomID WHERE Rooms.BuildingID=?;");
	$sth->execute([$buildingID]);
	return $sth->fetchAll(PDO::FETCH_ASSOC);
}
function getRoomsInBuilding($buildingID){
	$sth = $db->prepare("SELECT * FROM Rooms WHERE buildingID=?");
	$sth->execute([$buildingID]);
	return $sth->fetchAll(PDO::FETCH_ASSOC);
}
function getPointsOfTypeInBuilding($equipmentType, $buildingID){
	$sth = $db->prepare("SELECT * FROM Points INNER JOIN PointTypes ON 
		PointTypes.ID = Points.PointTypeID WHERE buildingID=? AND PointTypes.Name=?");
	$sth->execute([$buildingID, $equipmentType]);
	return $sth->fetchAll(PDO::FETCH_ASSOC);
}
function getValuesInRange($pointID, $start, $end){
	$sth = $db->prepare("SELECT * FROM PointValues WHERE PointID=? 
		AND PointTimestamp>? and PointTimestamp < ?");
	$sth->execute([$pointID, $start, $end]);
	return $sth->fetchAll(PDO::FETCH_ASSOC);
}
function getValue($pointID, $timestamp){
	$sth = $db->prepare("SELECT * FROM PointValues WHERE PointID=? 
		AND PointTimestamp=? and PointTimestamp < ?");
	$sth->execute([$pointID, $timestamp]);
	return $sth->fetch();
}
function getValuesByBuildingInRange($buildingID, $start, $end){
	$sth = $db->prepare("SELECT * FROM PointValues 
		INNER JOIN Points ON PointValues.PointID=Point.ID 
		INNER JOIN Rooms ON Rooms.ID = Points.RoomID 
		WHERE Rooms.BuildingID=? AND PointTimestamp>? and PointTimestamp < ?");
	$sth->execute([$buildingID, $start, $end]);
	return $sth->fetch();
}
function getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType){
	$sth = $db->prepare("SELECT * FROM PointValues 
		INNER JOIN Points ON PointValues.PointID=Point.ID 
		INNER JOIN Rooms ON Rooms.ID = Points.RoomID 
		INNER JOIN PointTypes ON PointTypes.ID=Points.PointTypeID 
		WHERE PointTypes.Name = ? AND Rooms.BuildingID=? 
		AND PointTimestamp>? and PointTimestamp < ?");
	$sth->execute([$equipmentType, $buildingID, $start, $end]);
	return $sth->fetchAll(PDO::FETCH_ASSOC);
}