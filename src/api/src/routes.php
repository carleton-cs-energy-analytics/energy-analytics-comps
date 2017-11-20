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
function transformData($data){
	foreach ($data as $row) {
		if($data[TYPE_COL] == FLOAT_TYPE){
			$data[DATA_COL] = $data[DATA_COL] / 10^$data[FACTOR_COL];
		}elseif ($data[TYPE_COL] == ENUM_TYPE) {
			# didn't see any examples of this in the code, so wasn't sure how to handle these
			# for now just returning unformatted
			continue;
		}else{
			# handle ints and unknown types by just returning the data unformatted
			continue;
		}
	}
	return $data;
}
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
	return transformData(Model::getValuesInRange($pointID, $start, $end));
}
function getValue($pointID, $timestamp){
	return transformData(Model::getValue($pointID, $timestamp));
}
function getValuesByBuildingInRange($buildingID, $start, $end){
	return transformData(Model::getValuesByBuildingInRange($buildingID, $start, $end));
}
function getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType){
	return transformData(Model::getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType));
}
