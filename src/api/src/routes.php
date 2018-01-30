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
$app->get('/point/:name', function ($name) {
    $result = getPointInfoByName($name);
    echo json_encode($result);
});
$app->get('/values/point/:id/:start/:end', function ($id, $start, $end) {
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
$app->get('/values/building/:id/:timestamp', function ($id, $timestamp) {
    $result = getBuildingValuesAtTime($id, $timestamp);
    echo json_encode($result);
});
$app->get('/values/:timestamp', function ($timestamp) {
    $result = getValuesAtTime($timestamp);
    echo json_encode($result);
});
$app->get('/values/building/:id/:start/:end/type/:type', function ($id, $start, $end, $type) {
    $result = getValuesByBuildingInRangeByType($id, $type, $start, $end);
    echo json_encode($result);
});
$app->get('/values/building/:id/:start/:end/source/:source', function ($id, $start, $end, $type) {
    $result = getValuesByBuildingInRangeBySource($id, $type, $start, $end);
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
function getPointInfoByName($name){
    return Model::getPointInfoByName($name);
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
function getBuildingValuesAtTime($buildingID, $timestamp){
    return transformData(Model::getBuildingValuesAtTime($buildingID, $timestamp));
}
function getValuesAtTime($timestamp){
    return transformData(Model::getValuesAtTime($timestamp));
}
function getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType){
    return transformData(Model::getValuesByBuildingInRangeByType($buildingID, $start, $end, $equipmentType));
}
function getValuesByBuildingInRangeBySource($buildingID, $start, $end, $source){
    return transformData(Model::getValuesByBuildingInRangeBySource($buildingID, $start, $end, $equipmentType));
}


function transformData($data){
    $result = [];
    foreach ($data as $row) {
        if($row[TYPE_COL] == FLOAT_TYPE){
            $row[DATA_COL] = $row[DATA_COL] / pow(10, $row[FACTOR_COL]);
        }elseif ($row[TYPE_COL] == ENUM_TYPE) {
            # didn't see any examples of this in the code, so wasn't sure how to handle these
            # for now just returning unformatted
            break;
        }else{
            # handle ints and unknown types by just returning the data unformatted
            break;
        }
        array_push($result, $row);
    }
    return $result;
}
