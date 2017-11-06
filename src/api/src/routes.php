<?php

use Slim\Http\Request;
use Slim\Http\Response;

// Routes


$app->get('/buildings/{name}', function (Request $request, Response $response, array $args) {
    // Sample log message
    $this->logger->info("Slim-Skeleton '/' route");
    $db = Database::getInstance();
    $sth = $db->prepare("SELECT * FROM buildings WHERE Name=?");
	$sth->execute([$args['name']]);

	$result = $sth->fetchAll(PDO::FETCH_ASSOC);
    return $response->withJson($result);
});