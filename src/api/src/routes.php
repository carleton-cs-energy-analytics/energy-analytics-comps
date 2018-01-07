<?php

use Slim\Http\Request;
use Slim\Http\Response;


$app->get('/', function () {
    echo 'API Homepage';
});
$app->get('/buildings', function () {
    $result = getBuildingIDs();
    echo json_encode($result);
});

$app->get('/building/:name', function ($name) {
    $result = getBuildingIDByName($name);
    echo json_encode($result);
});

$app->get('/building/:id/rooms', function ($id) {
    $result = getRoomsInBuilding($id);
    echo json_encode($result);
});
$app->get('/building/:id/points', function ($id) {
    $result = getPointsInBuilding($id);
    echo json_encode($result);
});
$app->get('/building/:id/points/:type', function ($id, $type) {
    $result = getPointsOfTypeInBuilding($type, $id);
    echo json_encode($result);
});
$app->get('/values/point/:id/:start/:end', function ($id, $start, $en) {
    $result = getValuesInRange($id, $start, $end);
    echo json_encode($result);
});
$app->get('/value/point/:id/:timestamp', function ($id, $timestamp) {
    $result = getValue($id, $timestamp);
    echo json_encode($result);
});
$app->get('/values/building/:id/:start/:end', function ($id, $start, $end) {
    $result = getValuesByBuildingInRange($id, $start, $end);
    echo json_encode($result);
});
$app->get('/values/building/:id/:start/:end/:type', function ($id, $start, $end, $type) {
    $result = getValuesByBuildingInRangeByType($id, $type, $start, $end);
    echo json_encode($result);
});

function getBuildingIDs(){
	return Model::getBuildingIDs();
}
function getBuildingIDByName($name){
	return Model::getBuildingIDByName($name);
}
function getRoomsInBuilding($buildingID){
	return Model::getRoomsInBuilding($buildingID);
}
function getPointsInBuilding($buildingID){
	return Model::getPointsInBuilding($buildingID);
}
function getPointsOfTypeInBuilding($equipmentType, $buildingID){
	return Model::getPointsOfTypeInBuilding($equipmentType, $buildingID);
}
function getValuesInRange($pointID, $start, $end){
	return Model::getValuesInRange($pointID, $start, $end);
}
function getValue($pointID, $timestamp){
	return Model::getValue($pointID, $timestamp);
}
function getValuesByBuildingInRange($buildingID, $start, $end){
	return Model::getValuesByBuildingInRange($buildingID, $start, $end);
}
function getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType){
	return Model::getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType);
}
