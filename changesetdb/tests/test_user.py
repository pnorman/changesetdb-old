from unittest import TestCase
from unittest.mock import Mock
from changesetdb.user import User, UserHandler


class UserTest(TestCase):
    def test_str(self):
        u = User("J Doe", 123)
        self.assertEqual(str(u), "J Doe (123)")


class UserHandlerTest(TestCase):
    def test_add(self):
        db = Mock()
        handler = UserHandler(db)
        u = User("J Doe", 123)
        handler.add(u)
        self.assertEqual(db.add_user.call_count, 1)
