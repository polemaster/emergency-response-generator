import math
import random
from datetime import timedelta

import numpy as np
from incident import Incident
from person import Officer, Victim
from places import RandomPlaceGenerator
from team import Team
from utils.constants import (
    DEFAULT_VEHICLE_SPEED,
    INCIDENT_RESOLUTION_TIME,
    MERCATOR_PER_METER,
    RANDOM_POS_STEP,
)
from utils.helpers import random_range
from utils.position import Position
from vehicle import Car, Motorbike, VehiclePosition


class City:
    def __init__(self, city_name, top_left, bottom_right):
        self.city_name = city_name
        self.top_left = top_left
        self.bottom_right = bottom_right


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

    def move_vehicle(self, vehicle):
        if vehicle.team == None:
            return

        DELTA_MERCATOR_MAIN = (
            self.simulation_timestep * DEFAULT_VEHICLE_SPEED * MERCATOR_PER_METER
        )

        if vehicle.assigned_incident == None and vehicle.is_resolving_incident == False:
            # Going randomly, not occupied
            delta_lng = 0
            delta_lat = 0

            axis = random.choice([True, False])
            direction = random.choice([-1, 1])

            distance = (
                random.randrange(
                    int(DELTA_MERCATOR_MAIN / RANDOM_POS_STEP * 0.75),
                    int(DELTA_MERCATOR_MAIN / RANDOM_POS_STEP * 1.25) + 1,
                    1,
                )
                * RANDOM_POS_STEP
            )

            # print(DELTA_MERCATOR_MAIN)
            if axis:
                delta_lng = distance * direction
            else:
                delta_lat = distance * direction

            # Check city boudaries

            if (
                vehicle.position.lng + delta_lng < vehicle.city.top_left.lng
                or vehicle.position.lng + delta_lng > vehicle.city.bottom_right.lng
                or vehicle.position.lat + delta_lat < vehicle.city.bottom_right.lat
                or vehicle.position.lat + delta_lat > vehicle.city.top_left.lat
            ):
                # We inverse the direction
                direction = -1 * direction

            vehicle.position.lng += delta_lng
            vehicle.position.lat += delta_lat
        elif (
            vehicle.assigned_incident != None and vehicle.is_resolving_incident == False
        ):
            # Goes to the incident

            d_lat = vehicle.assigned_incident.position.lat - vehicle.position.lat
            d_lng = vehicle.assigned_incident.position.lng - vehicle.position.lng
            dist_to_incident = math.sqrt((d_lat) ** 2 + (d_lng) ** 2)

            step_distance = (
                random.randrange(
                    int(DELTA_MERCATOR_MAIN / RANDOM_POS_STEP * 0.75),
                    int(DELTA_MERCATOR_MAIN / RANDOM_POS_STEP * 1.25) + 1,
                    1,
                )
                * RANDOM_POS_STEP
            )

            if step_distance > dist_to_incident:
                vehicle.position.lat = vehicle.assigned_incident.position.lat
                vehicle.position.lng = vehicle.assigned_incident.position.lng

                # Calculate arrival time depending on travelled distance to distance to incident proportions
                distances_ratio = dist_to_incident / step_distance

                vehicle.assigned_incident.arrival_datetime = (
                    self.current_time
                    + timedelta(seconds=self.simulation_timestep * distances_ratio)
                )

                vehicle.is_resolving_incident = True
                vehicle.time_till_resolved = random_range(
                    INCIDENT_RESOLUTION_TIME * 0.5, INCIDENT_RESOLUTION_TIME * 1.5
                )

                # print("Stop and handle incident, time left: ", vehicle.time_till_resolved)
            else:
                dir_lat = d_lat / dist_to_incident
                dir_lng = d_lng / dist_to_incident

                vehicle.position.lat += dir_lat * step_distance
                vehicle.position.lng += dir_lng * step_distance

                # print("Moved, distance to incident = ", dist_to_incident)
        elif (
            vehicle.assigned_incident != None and vehicle.is_resolving_incident == True
        ):
            # Is resolving incident
            vehicle.time_till_resolved -= self.simulation_timestep

            # print("counter decreases, time left = {}".format(vehicle.time_till_resolved))

            if vehicle.time_till_resolved <= 0:
                # Resolved Incident

                # print("Incident nr {} resolved".format(vehicle.assigned_incident.incident_id))

                # In seconds 30min => 1800s
                AVG_SATISFACTORY_ARRIVAL_TIME = 1800
                arrival_time = (
                    vehicle.assigned_incident.arrival_datetime
                    - vehicle.assigned_incident.report_datetime
                ).seconds

                # ratio = AVG_SATISFACTORY_ARRIVAL_TIME / arrival_time

                # satisfaction_score = clamp(random.gauss(5 * ratio, 10), 1, 10)
                satisfaction_score = 8

                vehicle.assigned_incident.victim_satisfaction = satisfaction_score

                vehicle.time_till_resolved = 0
                vehicle.is_resolving_incident = False
                vehicle.assigned_incident = None

                # TODO Move proportionally to the time left
                # TODO Update incident with satisfaction score

    def move_vehicles(self):
        for vehicle in self.vehicles:
            self.move_vehicle(vehicle)

    def generate_victims_for_incident(self, incident):
        victims_count = np.random.poisson(lam=0.4, size=1)[0] + 1

        for _ in range(victims_count):
            victim = Victim(len(self.victims), self.current_time)
            self.victims.append(victim)
            incident.victims.append(victim)

    def save_vehicle_positions(self):
        for vehicle in self.vehicles:
            pos_copy = Position(vehicle.position.lat, vehicle.position.lng)
            self.vehicle_positions.append(
                VehiclePosition(vehicle, pos_copy, self.current_time)
            )

    def count_vehicles(self):
        assigned = 0
        resolving = 0

        for vehicle in self.vehicles:
            if vehicle.assigned_incident != None:
                assigned += 1

            if vehicle.is_resolving_incident == True:
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
        for vehicle in self.vehicles:
            if vehicle.team != None:
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
            if officer.team == None:
                available.append(officer)

        if officer_count <= len(available):
            for i in range(officer_count):
                # print(len(available))
                team.append(available[i])
        else:
            for officer in available:
                team.append(officer)

        return team

    def assign_team(self, vehicle, city):
        # In seconds => 8 hours = 28800s
        AVARAGE_TEAM_TIME = 28800

        if vehicle.team == None:
            officers = self.get_city_officers(city)

            chosen_officers = self.select_officers_to_team(vehicle, officers)

            if len(chosen_officers) > 0:
                team = Team(vehicle, self.current_time, chosen_officers)
                vehicle.team = team
                vehicle.team_time = random_range(
                    AVARAGE_TEAM_TIME * 0.75, AVARAGE_TEAM_TIME * 1.25, 4000
                )
                self.teams.append(team)

                for officer in chosen_officers:
                    officer.team = team
            # else:
            # print("No more available officers")
        # else:
        #   print("vehicle is full")

    def assign_teams(self):
        for city in self.cities:
            # Assign officers to vehicles within the city

            # officers = self.get_city_officers(city)
            vehicles = self.get_city_vehicles(city)

            # print("Assign officers to vehicles within the city ", len(officers), len(vehicles))

            for vehicle in vehicles:
                self.assign_team(vehicle, city)

    def assign_vehicle_to_incident(self, incident):
        closest_vehicle = None  # self.vehicles[0]
        closest_dist = (
            0  # calculate_distance(incident.position, closest_vehicle.position)
        )

        for vehicle in self.vehicles:
            if (
                vehicle.assigned_incident == None
                and vehicle.is_resolving_incident == False
            ):
                distance = calculate_distance(incident.position, vehicle.position)

                if closest_vehicle == None or distance < closest_dist:
                    closest_dist = distance
                    closest_vehicle = vehicle

        # We know the closest vehicle to the incident, now we assign it

        if closest_vehicle != None:
            closest_vehicle.assigned_incident = incident
        # else:
        # print("All vehicles are currently occupied")

    def generate_incidents(self):
        avarage_incidents = self.simulation_timestep / 3600 * self.incidents_per_hour
        # Here, higher random range of 50%
        incidents_count = int(
            random_range(int(avarage_incidents * 0.5), int(avarage_incidents * 1.5), 1)
        )
        # print(incidents_count)

        for _ in range(incidents_count):
            place_gen = RandomPlaceGenerator()
            city_name, district_name, selected_point = place_gen.select_random_place()
            position = Position(selected_point[0], selected_point[1])

            incident_datetime = self.current_time + timedelta(
                seconds=self.simulation_timestep * random_range(0, 1, 1000)
            )
            # TODO Should add victims to incident

            incident = Incident(
                len(self.incidents),
                city_name,
                district_name,
                incident_datetime,
                None,
                position,
            )
            self.generate_victims_for_incident(incident)

            # TODO Should assign car team to incident and add victims
            self.assign_vehicle_to_incident(incident)

            self.incidents.append(incident)

    def simulate(self, start_datetime, end_datetime):
        time_diff = end_datetime - start_datetime
        iterations = int(time_diff.total_seconds() / self.simulation_timestep)

        timestep = timedelta(seconds=self.simulation_timestep)

        for i in range(iterations):
            self.save_vehicle_positions()

            self.generate_incidents()
            self.move_vehicles()

            self.update_teams()
            self.assign_teams()

            self.current_time = start_datetime + i * timestep
