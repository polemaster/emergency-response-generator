import random
from datetime import timedelta

from numpy import loadtxt
from utils.constants import MAX_OFFICER_AGE, MAX_OFFICER_HIRE_TIME, MIN_OFFICER_AGE
from utils.helpers import generate_phone_number, generate_random_date

names_male = loadtxt("./data/polish_male_firstnames.txt", dtype="str")
names_female = loadtxt("./data/polish_female_firstnames.txt", dtype="str")
surnames = loadtxt("./data/polish_surnames.txt", dtype="str")
genders = ["female", "male"]
ranks = [
    "Constable",
    "Senior constable",
    "Sergeant",
    "Senior sergeant",
    "Staff sergeant",
    "Junior aspirant",
    "Aspirant",
    "Senior aspirant",
    "Staff aspirant",
    "Deputy commissioner",
    "Commissioner",
    "Chief commissioner",
    "Deputy inspector",
    "Junior inspector",
    "Inspector",
    "Chief inspector",
    "Inspector general",
]


class Person:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.gender = None


def generate_personal_info():
    gender = random.choice(genders)
    surname = random.choice(surnames)
    first_name = ""

    if gender == "male":
        first_name = random.choice(names_male)
    else:
        first_name = random.choice(names_female)

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
        self.rank = random.choice(ranks)
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
