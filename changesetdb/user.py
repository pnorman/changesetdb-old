class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class UserHandler:
    def __init__(self, db):
        self.db = db

    def add(self, user):
        self.db.add_user(user)
