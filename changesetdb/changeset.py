class Changeset:
    def __init__(self, attr, tags):
        self.id = attr["id"]
        self.uid = attr.get("uid")
        self.created_at = attr["created_at"]
        self.closed_at = attr.get("closed_at")
        self.open = attr["open"]
        self.num_changes = attr["num_changes"]
        self.bounds = Box(attr.get("min_lon"), attr.get("min_lat"),
                          attr.get("max_lon"), attr.get("max_lat"))
        self.tags = tags


class ChangesetHandler:
    def __init__(self, db):
        self.db = db

    def add(self, cs):
        self.db.copy_changeset(cs)


class Box:
    def __init__(self, min_lon, min_lat, max_lon, max_lat):
        self.min_lon = min_lon
        self.min_lat = min_lat
        self.max_lon = max_lon
        self.max_lat = max_lat

    def __str__(self):
        # define left, right, bottom, top
        if self.min_lon is None or self.max_lon is None \
           or self.min_lat is None or self.max_lat is None:
            return "SRID=4326;POLYGON EMPTY"

        return ('''SRID=4326;POLYGON(({left} {bottom},{left} {top},'''
                '''{right} {top},{right} {bottom},{left} {bottom}))''')\
            .format(left=self.min_lon, right=self.max_lon,
                    bottom=self.min_lat, top=self.max_lat)
