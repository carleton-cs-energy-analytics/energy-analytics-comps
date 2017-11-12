import unittest
from src.datareaders.database_connection import DatabaseConnection
from src.datareaders.data_object_holders import Point, PointType
import mock

# psql -c 'create database travis_ci_test;' -U postgres
# Makes empty DB, now we run V1_createTables
# Then @ end of tests, we want to delete this DB

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.database_connection = DatabaseConnection()

    def tearDown(self):
        self.database_connection.close_connection()

    def test_this(self):
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_this_also(self):
        self.assertTrue(False)

    @mock.patch("DatabaseConnection.db.execute")
    def test_with_mock(self, mock_sql_db):
        sqlMock = mock.Mock()
        mock_sql_db.return_value = sqlMock
        self.database_connection.execute_and_commit()

    # def test_loadSummary(self):
    #     db = Mock()
    #     query = appModel.session.query.return_value
    #     query.from_statment.return_value = ["id"]
    #     point = Point("hi", "room 5", "LDC", 1, "Valve", "This is a point")
    #     self.database_connection.get_point_id(point)

    @mock.patch('code_to_test.sqlite3.connect')
    def test_database_drop_table_call(self, mock_sqlite3_connect):
        sqlite_execute_mock = mock.Mock()
        mock_sqlite3_connect.return_value = sqlite_execute_mock
        code_to_test.main()
        call = 'drop table if exists some_table;'
        sqlite_execute_mock.execute.assert_called_with(call)

if __name__ == "__main__":
    unittest.main()