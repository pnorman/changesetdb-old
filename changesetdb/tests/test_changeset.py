from unittest import TestCase
from changesetdb.changeset import Box


class BoxTest(TestCase):
    def test_init(self):
        b = Box(-2, -1, 2, 1)
        self.assertEqual(b.min_lon, -2)
        self.assertEqual(b.min_lat, -1)
        self.assertEqual(b.max_lon, 2)
        self.assertEqual(b.max_lat, 1)

    def test_str(self):
        b = Box(-2, -1, 2, 1)
        self.assertEqual(str(b),
                         "SRID=4326;POLYGON((-2 -1,-2 1,2 1,2 -1,-2 -1))")

    def test_empty(self):
        b = Box(None, None, None, None)
        self.assertEqual(str(b), "SRID=4326;POLYGON EMPTY")
