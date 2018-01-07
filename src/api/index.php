<?php
if (PHP_SAPI == 'cli-server') {
    // To help the built-in PHP dev server, check if the request was actually for
    // something which should probably be served as a static file
    $url  = parse_url($_SERVER['REQUEST_URI']);
    $file = __DIR__ . $url['path'];
    if (is_file($file)) {
        return false;
    }
}
define('ENERGY_COMPS', '1');
error_reporting(E_ALL);
ini_set('display_errors', 1);

require __DIR__ . '/vendor/autoload.php';

session_start();

// Instantiate the app
$settings = require __DIR__ . '/src/settings.php';
$app = new \Slim\Slim($settings);

// DB Settings
require __DIR__.'/src/config.php';

// Register the model
require __DIR__ . '/src/model.php';

// Register database
require __DIR__ . '/src/database.php';

// Register routes
require __DIR__ . '/src/routes.php';

// Run app
$app->run();
