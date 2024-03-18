# In seconds +- 50%
# 25 minutes

import random
from datetime import timedelta

from utils.constants import EARLIEST_CAR_YEAR, OLDEST_CAR_YEAR
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
