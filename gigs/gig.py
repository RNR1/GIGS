class Gig:
    """A sample User class"""

    def __init__(self, user_id, date, time, venue, event, city, state, country):
        self.user_id = user_id
        self.date = date
        self.time = time
        self.venue = venue
        self.event = event
        self.location = {'city': city, 'state': state, 'country': country}
        

    
    def __repr__(self):
        return "Gig('{}', '{}', '{}', '{}', '{}', '{}')".format(self.user_id, self.date, self.time, self.venue, self.event, self.location)