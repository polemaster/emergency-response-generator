import math
import random
from datetime import timedelta
from utils.constants import MERCATOR_PER_METER

def generate_phone_number():
    first_digit = random.choice(["4", "5", "6", "7", "8"])
    other_digits = "".join(random.choices("0123456789", k=8))

    return first_digit + other_digits


def generate_random_date(start_date, end_date):
    date_range = end_date - start_date

    random_days = random.randint(0, date_range.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date


def generate_license_plate(city):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "0123456789"
    
    return "".join(
        [city.city_name[0]]
        + [random.choice(chars) for i in range(2)]
        + [random.choice(nums) for i in range(3)]
        + [random.choice(chars) for i in range(2)]
    )


# Both ends included
def random_range(start, end, INTERNAL_SUBSTEPS=1000):
    return (
        random.randrange(
            int(start * INTERNAL_SUBSTEPS), int(end * INTERNAL_SUBSTEPS) + 1, 1
        )
        / INTERNAL_SUBSTEPS
    )

def latlngToMeters(lat, lng):
    "Convert lat,lng degrees to meters in Web Mercator projection. 0,0 is at top left corner"
    radius = 6378137.0 # WGS84 equatorial radius (meters) - used in spherical projection
    
    lat = math.radians(lat)
    lng = math.radians(lng)
    x = radius * (math.pi + lng)
    y = radius * (math.pi - math.log(math.tan(math.pi/4 + lat/2)))
    return x, y

def calculate_distance(pos_1, pos_2):
    x_1, y_1 = latlngToMeters(pos_1.lat, pos_1.lng)
    x_2, y_2 = latlngToMeters(pos_2.lat, pos_2.lng)
    
    return math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)


def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n