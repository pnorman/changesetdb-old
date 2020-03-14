from unittest import TestCase
from unittest.mock import Mock
from changesetdb.parser import Parser


class ParserTest(TestCase):
    def test_creates_connection(self):
        db = Mock()
        p = Parser(False, db)
        self.assertEqual(p.diff_mode, False)
