<?php

use Slim\Http\Request;
use Slim\Http\Response;

// Routes

$app->get('/buildings/{name}', function (Request $request, Response $response, array $args) {
    // Sample log message
    $this->logger->info("Slim-Skeleton '/' route");
    $dbSettings = $container->get('settings')['database'];
    $dbh = new PDO(
    	"pgsql:dbname=".$dbSettings['dbname'].";host=".$dbSettings['host'],
    	$dbSettings['username'], 
    	$dbSettings['password']
    ); 
    $sth = $dbh->prepare("SELECT * FROM buildings WHERE Name=?");
	$sth->execute([$args['name']]);

	$result = $sth->fetchAll();
    return $response->withJson($result);
});