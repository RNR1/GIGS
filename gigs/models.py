class User:

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

class Gig:

    def __init__(self, user_id, date, time, venue, event, city, state, country):
        self.user_id = user_id
        self.date = date
        self.time = time
        self.venue = venue
        self.event = event
        self.location = {'city': city, 'state': state, 'country': country}
           
    def __repr__(self):
        return "Gig('{}', '{}', '{}', '{}', '{}', '{}')".format(self.user_id, self.date, self.time, self.venue, self.event, self.location)