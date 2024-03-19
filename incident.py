from datetime import timedelta

from utils.constants import CODES
from utils.helpers import random_range
from utils.position import Position


class Incident:
    def __init__(self, id, current_time, simulation_timestep, place_gen):

        city_name, district_name, selected_point = place_gen.select_random_place()
        position = Position(selected_point[0], selected_point[1])

        incident_datetime = current_time + timedelta(
            seconds=simulation_timestep * random_range(0, 1, 1000)
        )

        self.incident_id = id
        self.city = city_name
        self.district = district_name
        self.report_datetime = incident_datetime
        self.arrival_datetime = None
        self.victim_satisfaction = None
        self.position = position
        self.type_code = CODES["type_code"].sample().values[0]

        self.victims = list()


class IncidentTeamAssignments:
    def __init__(self, incident_id, team_id):
        self.incident_id = incident_id
        self.team_id = team_id


class VictimGroups:
    def __init__(self, victim_id, incident_id):
        self.victim_id = victim_id
        self.incident_id = incident_id
