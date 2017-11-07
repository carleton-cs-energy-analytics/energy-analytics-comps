<?php

use Slim\Http\Request;
use Slim\Http\Response;

// Routes

$app->get('/buildings', function (Request $request, Response $response, array $args) {
    $result = getBuildingIDs();
    return $response->withJson($result);
});

$app->get('/building/{name}', function (Request $request, Response $response, array $args) {
    $result = getBuildingIDByName($args['name']);
    return $response->withJson($result);
});

$app->get('/building/{id}/rooms', function (Request $request, Response $response, array $args) {
    $result = getRoomsInBuilding($args['id']);
    return $response->withJson($result);
});
$app->get('/building/{id}/points', function (Request $request, Response $response, array $args) {
    $result = getPointsInBuilding($args['id']);
    return $response->withJson($result);
});
$app->get('/building/{id}/points/{type}', function (Request $request, Response $response, array $args) {
    $result = getPointsOfTypeInBuilding($args['type'], $args['id']);
    return $response->withJson($result);
});
$app->get('/values/point/{id}/{start}/{end}', function (Request $request, Response $response, array $args) {
    $result = getValuesInRange($args['id'], $args['start'], $args['end']);
    return $response->withJson($result);
});
$app->get('/value/point/{id}/{timestamp}', function (Request $request, Response $response, array $args) {
    $result = getValue($args['id'], $args['timestamp']);
    return $response->withJson($result);
});
$app->get('/values/building/{id}/{start}/{end}', function (Request $request, Response $response, array $args) {
    $result = getValuesByBuildingInRange($args['id'], $args['start'], $args['end']);
    return $response->withJson($result);
});
$app->get('/values/building/{id}/{start}/{end}/{type}', function (Request $request, Response $response, array $args) {
    $result = getValuesByBuildingInRangeByType($args['id'], $args['type'], $args['start'], $args['end']);
    return $response->withJson($result);
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
