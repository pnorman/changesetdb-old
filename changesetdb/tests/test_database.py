from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from changesetdb.database import Database
from changesetdb.user import User


class DatabaseTest(TestCase):
    @patch('psycopg2.extras.register_hstore')
    @patch('psycopg2.connect')
    def test_create(self, mock_connect, mock_register_hstore):
        Database("dbname", "host", "port", "username")
        mock_connect.assert_called_with(dbname="dbname", host="host",
                                        port="port", username="username")
        self.assertEqual(mock_register_hstore.called, True)

    @patch('psycopg2.extras.register_hstore')
    @patch('psycopg2.connect')
    def test_createtables(self, mock_connect, mock_register_hstore):
        mock_cur = mock_connect.return_value.cursor.return_value
        mock_cur.execute = Mock()
        Database("dbname", "host", "port", "username").createtables()
        self.assertEqual(mock_cur.execute.call_count, 5)
        mock_connect.return_value.commit.assert_called_with()

    @patch('psycopg2.extras.register_hstore')
    @patch('psycopg2.connect')
    def test_droptables(self, mock_connect, mock_register_hstore):
        mock_cur = mock_connect.return_value.cursor.return_value
        mock_cur.execute = Mock()
        Database("dbname", "host", "port", "username").droptables()
        self.assertEqual(mock_cur.execute.call_count, 1)
        mock_connect.return_value.commit.assert_called_with()

    @patch('psycopg2.extras.register_hstore')
    @patch('psycopg2.connect')
    def test_add_user(self, mock_connect, mock_register_hstore):
        mock_cur = mock_connect.return_value.cursor.return_value
        mock_cur.execute = Mock()
        Database("dbname", "host", "port", "username")\
            .add_user(User("J Doe", 123))
        self.assertEqual(mock_cur.execute.call_count, 1)
        mock_connect.return_value.commit.assert_called_with()
