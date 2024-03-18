class Team:
    def __init__(self, team_id, vehicle, start_datetime, officers):

        self.team_id = team_id
        self.vehicle = vehicle
        self.start_datetime = start_datetime
        self.end_datetime = None

        self.officers = officers
