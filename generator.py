import random
from datetime import timedelta

import numpy as np
from city import City
from incident import Incident, IncidentTeamAssignments, VictimGroups
from person import Officer, Victim
from places import RandomPlaceGenerator
from team import Team
from utils.constants import AVERAGE_TEAM_TIME, AVG_INSPECTIONS_SPAN
from utils.constants import AVERAGE_TEAM_TIME, AVG_INSPECTIONS_SPAN
from utils.helpers import calculate_distance, random_range, clamp
from utils.constants import AVERAGE_TEAM_TIME
from utils.helpers import calculate_distance, clamp, random_range
from utils.position import Position
from vehicle import Car, Motorbike, VehiclePosition


class Generator:
    def __init__(
        self, initial_counts, initial_date, simulation_timestep, incidents_per_hour
    ):
        self.initial_counts = initial_counts

        # In seconds
        self.simulation_timestep = simulation_timestep
        self.incidents_per_hour = incidents_per_hour

        self.vehicles = list()
        self.officers = list()

        self.incidents = list()
        self.victims = list()

        self.teams = list()
        self.vehicle_positions = list()

        self.incident_team_assignments = list()
        self.victim_groups = list()

        self.current_time = initial_date

        self.cities = list()

        # city, top_left_latitude, top_left_longitude, bottom_right_latitude,  bottom_right_longitude
        # Gdańsk: 54.44725173693497,  18.44234779682661,  54.2749,  18.9362
        # Warszawa: 52.3657,  20.8515,  52.1033,  21.2690
        # Kraków: 50.1233, 19.8094,  49.9737,  20.2150

        self.cities.append(
            City(
                "Gdansk",
                Position(54.44725173693497, 18.44234779682661),
                Position(54.2749, 18.9362),
            )
        )
        self.cities.append(
            City("Warszawa", Position(52.3657, 20.8515), Position(52.1033, 21.2690))
        )
        self.cities.append(
            City("Krakow", Position(50.1233, 19.8094), Position(49.9737, 20.2150))
        )

        self.place_gen = RandomPlaceGenerator()

    def generate_initial_data(self):
        for c_i, city in enumerate(self.cities):
            for i in range(0, self.initial_counts["officers"][c_i]):
                officer = Officer(i, city, self.current_time)
                self.officers.append(officer)

            for i in range(0, self.initial_counts["cars"][c_i]):
                car = Car(city, self.current_time)
                self.vehicles.append(car)

            for i in range(0, self.initial_counts["motorbikes"][c_i]):
                motorbike = Motorbike(city, self.current_time)
                self.vehicles.append(motorbike)

    def move_vehicles(self):
        for vehicle in self.vehicles:
            vehicle.move_vehicle(self.simulation_timestep, self.current_time)

    def generate_victims_for_incident(self, incident):
        victims_count = np.random.poisson(lam=0.4, size=1)[0] + 1

        for _ in range(victims_count):
            victim = Victim(len(self.victims), self.current_time)

            victim_grouping = VictimGroups(victim.victim_id, incident.incident_id)
            self.victim_groups.append(victim_grouping)

            self.victims.append(victim)
            incident.victims.append(victim)

    def update_vehicles_data(self):
    def update_vehicles_data(self):
        for vehicle in self.vehicles:
            self.vehicle_positions.append(
                VehiclePosition(
                    len(self.vehicle_positions),
                    vehicle.license_plate_number,
                    vehicle.position.lat,
                    vehicle.position.lng,
                    self.current_time,
                )
            )

    def count_vehicles(self):
        assigned = 0
        resolving = 0

        for vehicle in self.vehicles:
            if vehicle.assigned_incident is not None:
                assigned += 1

            if vehicle.is_resolving_incident:
                resolving += 1

    def get_city_officers(self, city):
        result = list()
        for officer in self.officers:
            if officer.city == city:
                result.append(officer)

        return result

    def get_city_vehicles(self, city):
        result = list()
        for vehicle in self.vehicles:
            if vehicle.city == city:
                result.append(vehicle)

        return result

    def update_teams(self):
        # Iterate through all current teams
        for vehicle in self.vehicles:
            if vehicle.team is not None:
                if vehicle.team_time <= 0:
                    # FIX END DATE could be varying within timestep
                    vehicle.team.end_datetime = self.current_time
                    # print("team disapears at ", vehicle.team.end_datetime)

                    for officer in vehicle.team.officers:
                        officer.team = None

                    vehicle.team = None
                    # TODO Could add some cooldown for the vehicle
                else:
                    vehicle.team_time -= self.simulation_timestep

    def select_officers_to_team(self, vehicle, officers):
        team = list()
        available = list()

        officer_count = 1
        if isinstance(vehicle, Car):
            officer_count = random.choice([1, 2, 3])

        for officer in officers:
            if officer.team is None:
                available.append(officer)

        if officer_count <= len(available):
            for i in range(officer_count):
                # print(len(available))
                team.append(available[i])
        else:
            for officer in available:
                team.append(officer)

        return team

    def assign_team(self, vehicle):
        # In seconds => 8 hours = 28800s

        if vehicle.team is None:
            officers = self.get_city_officers(vehicle.city)

            chosen_officers = self.select_officers_to_team(vehicle, officers)

            if len(chosen_officers) > 0:
                team = Team(
                    len(self.teams),
                    self.current_time,
                    vehicle.license_plate_number,
                    chosen_officers,
                )
                vehicle.team = team
                vehicle.team_time = random_range(
                    AVERAGE_TEAM_TIME * 0.75, AVERAGE_TEAM_TIME * 1.25, 4000
                )
                self.teams.append(team)

                for officer in chosen_officers:
                    officer.team = team
            # else:
            # print("No more available officers")
        # else:
        #   print("vehicle is full")

    def assign_teams(self):
        for vehicle in self.vehicles:
            self.assign_team(vehicle)

    def assign_vehicle_to_incident(self, incident):
        closest_vehicle = None  # self.vehicles[0]
        closest_dist = 0

        for vehicle in self.vehicles:
            if (
                vehicle.assigned_incident is None
                and vehicle.team
                and not vehicle.is_resolving_incident
            ):
                distance = calculate_distance(incident.position, vehicle.position)

                if closest_vehicle is None or distance < closest_dist:
                    closest_dist = distance
                    closest_vehicle = vehicle

        # We know the closest vehicle to the incident, now we assign it

        if closest_vehicle is not None:
            closest_vehicle.assigned_incident = incident

            incident_team_assignment = IncidentTeamAssignments(
                incident.incident_id, closest_vehicle.team.team_id
            )
            self.incident_team_assignments.append(incident_team_assignment)
        else:
            print("All vehicles are currently occupied")

    def generate_incidents(self):
        avarage_incidents = self.simulation_timestep / 3600 * self.incidents_per_hour
        # Here, higher random range of 50%
        incidents_count = int(
            random_range(int(avarage_incidents * 0.5), int(avarage_incidents * 1.5))
        )
        # print(incidents_count)

        for _ in range(incidents_count):
            # TODO Should add victims to incident

            incident = Incident(
                len(self.incidents),
                self.current_time,
                self.simulation_timestep,
                self.place_gen,
            )
            self.generate_victims_for_incident(incident)

            required_teams_count = clamp(
                np.random.poisson(lam=0.3, size=1)[0] + 1, 1, 3
            )
            # print(required_teams_count)

            for _ in range(required_teams_count):
                self.assign_vehicle_to_incident(incident)

            self.incidents.append(incident)

    def simulate(self, start_datetime, end_datetime):
        time_diff = end_datetime - start_datetime
        iterations = int(time_diff.total_seconds() / self.simulation_timestep)

        timestep = timedelta(seconds=self.simulation_timestep)

        self.current_time = start_datetime

        for _ in range(iterations):
            self.update_vehicles_data()

            self.generate_incidents()
            self.move_vehicles()

            self.update_teams()
            self.assign_teams()

            self.current_time += timestep
