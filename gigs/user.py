class User:
    """A sample User class"""

    def __init__(self, email, display, first, last, city, state, country, bio):
        self.email = email
        self.display = display
        self.first = first
        self.last = last
        self.location = {'city': city, 'state': state, 'country': country}
        self.bio = bio

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "User('{}', '{}', '{}', '{}', '{}', '{}')".format(self.email, self.display, self.first, self.last, self.location, self.bio)