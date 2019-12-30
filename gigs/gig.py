class Gig:
    """A sample User class"""

    def __init__(self, user, date, time, venue, event, city, state, country):
        self.user = user
        self.date = date
        self.time = time
        self.venue = venue
        self.event = event
        self.location = {'city': city, 'state': state, 'country': country}
        

    
    def __repr__(self):
        return "User('{}', '{}', '{}', '{}', '{}', '{}')".format(self.user, self.date, self.time, self.venue, self.event, self.location)