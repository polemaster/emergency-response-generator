class Team:
    def __init__(self, vehicle, start_datetime, officers):

        self.vehicle = vehicle
        self.start_datetime = start_datetime
        self.end_datetime = None

        self.officers = officers
