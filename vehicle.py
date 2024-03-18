# In seconds +- 50%
# 25 minutes

import math
import random
from datetime import timedelta

from utils.constants import (
    DEFAULT_VEHICLE_SPEED,
    EARLIEST_CAR_YEAR,
    INCIDENT_RESOLUTION_TIME,
    MERCATOR_PER_METER,
    OLDEST_CAR_YEAR,
    RANDOM_POS_STEP,
)
from utils.helpers import generate_licence_plate, generate_random_date, random_range
from utils.position import Position


class Vehicle:
    def __init__(self, city, current_time):

        self.license_plate_number = generate_licence_plate()

        # "car" or "motorbike"
        # self.vehicle_type = vehicle_type
        self.brand = None
        self.model = None
        self.manufacturing_year = generate_random_date(
            current_time - timedelta(days=OLDEST_CAR_YEAR * 365),
            current_time - timedelta(days=EARLIEST_CAR_YEAR * 365),
        )

        # FIX it - just an testing position
        lng = random_range(city.top_left.lng, city.bottom_right.lng, 10000)
        lat = random_range(city.bottom_right.lat, city.top_left.lat, 10000)
        position = Position(lat, lng)
        self.position = position

        self.last_inspection = self.manufacturing_year

        self.assigned_incident = None
        self.is_resolving_incident = False
        self.time_till_resolved = 0

        self.team = None
        self.city = city

        # In seconds, 0 = to be freed
        self.team_time = 0

    def move_vehicle(self, simulation_timestep, current_time):
        if self.team is None:
            return

        DELTA_MERCATOR_MAIN = (
            simulation_timestep * DEFAULT_VEHICLE_SPEED * MERCATOR_PER_METER
        )

        if self.assigned_incident is None and not self.is_resolving_incident:
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
                self.position.lng + delta_lng < self.city.top_left.lng
                or self.position.lng + delta_lng > self.city.bottom_right.lng
                or self.position.lat + delta_lat < self.city.bottom_right.lat
                or self.position.lat + delta_lat > self.city.top_left.lat
            ):
                # We inverse the direction
                direction = -1 * direction

            self.position.lng += delta_lng
            self.position.lat += delta_lat
        elif self.assigned_incident is not None and not self.is_resolving_incident:
            # Goes to the incident

            d_lat = self.assigned_incident.position.lat - self.position.lat
            d_lng = self.assigned_incident.position.lng - self.position.lng
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
                self.position.lat = self.assigned_incident.position.lat
                self.position.lng = self.assigned_incident.position.lng

                # Calculate arrival time depending on travelled distance to distance to incident proportions
                distances_ratio = dist_to_incident / step_distance

                self.assigned_incident.arrival_datetime = current_time + timedelta(
                    seconds=simulation_timestep * distances_ratio
                )

                self.is_resolving_incident = True
                self.time_till_resolved = random_range(
                    INCIDENT_RESOLUTION_TIME * 0.5, INCIDENT_RESOLUTION_TIME * 1.5
                )

                # print("Stop and handle incident, time left: ", vehicle.time_till_resolved)
            else:
                dir_lat = d_lat / dist_to_incident
                dir_lng = d_lng / dist_to_incident

                self.position.lat += dir_lat * step_distance
                self.position.lng += dir_lng * step_distance

                # print("Moved, distance to incident = ", dist_to_incident)
        elif self.assigned_incident is not None and self.is_resolving_incident:
            # Is resolving incident
            self.time_till_resolved -= simulation_timestep

            # print("counter decreases, time left = {}".format(vehicle.time_till_resolved))

            if self.time_till_resolved <= 0:
                # Resolved Incident

                # print("Incident nr {} resolved".format(vehicle.assigned_incident.incident_id))

                # In seconds 30min => 1800s
                AVG_SATISFACTORY_ARRIVAL_TIME = 1800
                arrival_time = (
                    self.assigned_incident.arrival_datetime
                    - self.assigned_incident.report_datetime
                ).seconds

                # ratio = AVG_SATISFACTORY_ARRIVAL_TIME / arrival_time

                # satisfaction_score = clamp(random.gauss(5 * ratio, 10), 1, 10)
                satisfaction_score = 8

                self.assigned_incident.victim_satisfaction = satisfaction_score

                self.time_till_resolved = 0
                self.is_resolving_incident = False
                self.assigned_incident = None

                # TODO Move proportionally to the time left
                # TODO Update incident with satisfaction score


class Car(Vehicle):
    def __init__(self, city, current_time):
        super().__init__(city, current_time)
        self.brand = random.choice(list(car_brands.keys()))
        self.model = random.choice(car_brands[self.brand])


class Motorbike(Vehicle):
    def __init__(self, city, current_time):
        super().__init__(city, current_time)
        self.brand = random.choice(list(motorbike_brands.keys()))
        self.model = random.choice(motorbike_brands[self.brand])


class VehiclePosition:
    def __init__(self, vehicle, position, time):

        self.vehicle = vehicle
        self.position = position
        self.time = time


car_brands = {
    "Bmw": ["Series 3"],
    "Toyota": ["Corolla", "Land Cruiser", "Hilux", "Rav"],
    "Skoda": ["Superb"],
    "Kia": ["Stinger GT", "Ceed 3"],
    "Volkswagen": ["Crafter", "Passat"],
    "Hyundai": ["Ionia", "Tucson"],
}

motorbike_brands = {
    "Triumph": ["Tiger 1050"],
    "Kawasaki": ["Versys 1000"],
    "BMW": ["R 1250 RT"],
}
