import pandas as pd
from numpy import loadtxt

# In order of cities
INITIAL_COUNTS = {
    "officers": [60, 80, 50],
    "cars": [35, 50, 45],
    "motorbikes": [10, 15, 5],
}

# Ratio representing 1 meter in latitude/longitude scale
MERCATOR_PER_METER = 2.245789145352464e-6

# 30 meters
RANDOM_POS_STEP = MERCATOR_PER_METER * 30

# In seconds => 25 minutes
INCIDENT_RESOLUTION_TIME = 1500 

# All 3 in years
MIN_OFFICER_AGE = 21
MAX_OFFICER_AGE = 70
MAX_OFFICER_HIRE_TIME = 35


OLDEST_CAR_YEAR = 10
EARLIEST_CAR_YEAR = 1

# In m/s => ~50km/h
DEFAULT_VEHICLE_SPEED = 14

# Average time between inspections in seconds
AVG_INSPECTIONS_SPAN = int(1.2 * 365 * 24 * 3600)

# In seconds => 8h 
AVERAGE_TEAM_TIME = 28800 

# load names
NAMES_MALE = loadtxt("./data/polish_male_firstnames.txt", dtype="str")
NAMES_FEMALE = loadtxt("./data/polish_female_firstnames.txt", dtype="str")
LAST_NAMES = loadtxt("./data/polish_surnames.txt", dtype="str")

GENDERS = ["female", "male"]
RANKS = [
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

# load incident types
CODES_FILEPATH = "data/codes.csv"
CODES = pd.read_csv(CODES_FILEPATH)
