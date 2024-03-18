from datetime import datetime

from generator import Generator
from utils.constants import INITIAL_COUNTS


def main():
    import time

    start = time.time()

    startdate = datetime(2023, 1, 1)
    enddate = datetime(2023, 1, 31)

    generator = Generator(INITIAL_COUNTS, startdate, 600, 16)
    generator.generate_initial_data()

    generator.assign_teams()

    generator.simulate(startdate, enddate)

    end = time.time()
    print("Time:", end - start)


if __name__ == "__main__":
    main()
