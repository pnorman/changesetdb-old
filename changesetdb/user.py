class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class UserHandler:
    def __init__(self):
        ''' Take in DB stuff, set up a user cache'''
        pass

    def add(self, user):
        print("Saving user {}".format(str(user)))