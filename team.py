class Team:
    def __init__(self, team_id, start_datetime, license_plate_number, officers):

        self.team_id = team_id
        self.start_datetime = start_datetime
        self.end_datetime = None
        self.license_plate_number = license_plate_number

        self.officers = officers
