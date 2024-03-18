import math
import random
from datetime import timedelta


def generate_phone_number():
    area_codes = ["12", "13"]

    area_code = random.choice(area_codes)
    number = "".join(random.choices("0123456789", k=7))

    return f"{area_code} {number[:3]} {number[3:]}"


def generate_random_date(start_date, end_date):
    date_range = end_date - start_date

    random_days = random.randint(0, date_range.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date


def generate_licence_plate():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "0123456789"

    return "".join(
        [random.choice(chars) for i in range(3)]
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


def calculate_distance(pos_1, pos_2):
    return math.sqrt((pos_1.lat - pos_2.lat) ** 2 + (pos_1.lng - pos_2.lng) ** 2)


def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


if __name__ == "__main__":
    main()
