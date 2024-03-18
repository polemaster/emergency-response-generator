import random
from datetime import timedelta

from utils.constants import (
    GENDERS,
    LAST_NAMES,
    MAX_OFFICER_AGE,
    MAX_OFFICER_HIRE_TIME,
    MIN_OFFICER_AGE,
    NAMES_FEMALE,
    NAMES_MALE,
    RANKS,
)
from utils.helpers import generate_phone_number, generate_random_date


class Person:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.gender = None


def generate_personal_info():
    gender = random.choice(GENDERS)
    surname = random.choice(LAST_NAMES)
    first_name = ""

    if gender == "male":
        first_name = random.choice(NAMES_MALE)
    else:
        first_name = random.choice(NAMES_FEMALE)

    return {"gender": gender, "first_name": first_name, "last_name": surname}


class Officer:
    def __init__(self, id, city, current_time):

        personal_info = generate_personal_info()

        hire_date = generate_random_date(
            current_time - timedelta(days=MAX_OFFICER_HIRE_TIME * 365),
            current_time,
        )

        date_of_birth = generate_random_date(
            current_time - timedelta(days=MAX_OFFICER_AGE * 365),
            hire_date - timedelta(days=MIN_OFFICER_AGE * 365),
        )

        self.officer_id = id
        self.first_name = personal_info["first_name"]
        self.last_name = personal_info["last_name"]
        self.rank = random.choice(RANKS)
        self.gender = personal_info["gender"]
        self.date_of_birth = date_of_birth
        self.hire_date = hire_date
        self.email = "officer{}@police.org.pl".format(id)
        self.phone_number = generate_phone_number()

        self.city = city

        self.team = None


class Victim:
    def __init__(self, victim_id, current_time):
        personal_info = generate_personal_info()

        date_of_birth = generate_random_date(
            current_time - timedelta(days=90 * 365),
            current_time - timedelta(days=2 * 365),
        )

        self.victim_id = victim_id
        self.first_name = personal_info["first_name"]
        self.last_name = personal_info["last_name"]
        self.gender = personal_info["gender"]
        self.date_of_birth = date_of_birth
