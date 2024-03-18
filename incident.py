class Incident:
    def __init__(
        self, incident_id, city, district, report_datetime, description, position
    ):

        self.incident_id = incident_id
        self.city = city
        self.district = district
        self.report_datetime = report_datetime
        self.arrival_datetime = None
        self.victim_satisfaction = None
        self.description = description
        self.incident_type = None
        self.position = position

        self.victims = list()


class IncidentTeamAssignments:
    def __init__(self):
        self.team = None
        self.incident = None


class VictimGroups:
    def __init__(self):
        self.victim = None
        self.incident = None
