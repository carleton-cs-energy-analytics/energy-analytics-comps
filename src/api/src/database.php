<?php
/*
* Database Class
* Just a singleton class so we don't open multiple connections accidentally (expensive)
*/
class Database{
    public $db;
    private static $instance;
    private function __construct() {
        $this->db = new PDO(
            "pgsql:dbname=".DB_NAME.";host=".DB_HOST,
            DB_USERNAME, 
            DB_PASSWORD
        );
    }
    public static function getInstance() {
        if (!isset(self::$instance))
        {
            self::$instance = new Database();
        }
        return self::$instance->db;
    }
}