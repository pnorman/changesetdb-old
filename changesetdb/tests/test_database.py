from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from changesetdb.database import Database


class DatabaseTest(TestCase):
    @patch('psycopg2.connect')
    def test_creates_connection(self, mock_connect):
        Database("dbname", "host", "port", "username")
        mock_connect.assert_called_with(dbname="dbname", host="host",
                                        port="port", username="username")

    @patch('psycopg2.connect')
    def test_createtables(self, mock_connect):
        mock_cur = mock_connect.return_value.cursor.return_value
        mock_cur.execute = Mock()
        Database("dbname", "host", "port", "username").createtables()
        self.assertEqual(mock_cur.execute.call_count, 5)
        mock_connect.return_value.commit.assert_called_with()

    @patch('psycopg2.connect')
    def test_droptables(self, mock_connect):
        mock_cur = mock_connect.return_value.cursor.return_value
        mock_cur.execute = Mock()
        Database("dbname", "host", "port", "username").droptables()
        self.assertEqual(mock_cur.execute.call_count, 1)
        mock_connect.return_value.commit.assert_called_with()
