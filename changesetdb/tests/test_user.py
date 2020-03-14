from unittest import TestCase
from changesetdb.user import User


class UserTest(TestCase):
    def test_str(self):
        u = User("J Doe", 123)
        self.assertEqual(str(u), "J Doe (123)")
