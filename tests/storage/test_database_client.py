import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from app.storage.database_client import DatabaseClient
from app.utils.constants import DATABASE_NAME


class TestDatabaseClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.patcher = patch('sqlite3.connect')
        cls.mock_connect = cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def setUp(self):
        # Create new mock objects for each test
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Reset the mock_connect for each test
        self.mock_connect.reset_mock()
        self.mock_connect.side_effect = None
        self.mock_connect.return_value = self.mock_conn

    def test_create_database_success(self):
        client = DatabaseClient()
        result = client.create_database()

        self.mock_connect.assert_called_once_with(DATABASE_NAME)
        self.assertEqual(self.mock_cursor.execute.call_count, 2)
        self.mock_conn.commit.assert_called_once()
        self.assertEqual(result, self.mock_conn)

    def test_create_database_sqlite_error(self):
        self.mock_connect.side_effect = sqlite3.Error("Test error")

        client = DatabaseClient()
        with self.assertRaises(sqlite3.Error) as context:
            client.create_database()

        self.assertTrue("An error occurred: Test error" in str(context.exception))

    def test_create_database_rollback_on_error(self):
        self.mock_cursor.execute.side_effect = sqlite3.Error("Test error")

        client = DatabaseClient()
        with self.assertRaises(sqlite3.Error):
            client.create_database()

        self.mock_conn.rollback.assert_called_once()

    def test_database_client_interface(self):
        self.assertTrue(hasattr(DatabaseClient, 'create_database'))
        self.assertTrue(callable(getattr(DatabaseClient, 'create_database')))
