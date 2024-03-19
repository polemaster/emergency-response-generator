import random
from datetime import datetime

from exporter import Exporter
from generator import Generator
from utils.constants import INITIAL_COUNTS


def main():
    random.seed(42)
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

    start = time.time()

    # write_incidents_to_csv(generator.incidents, "generated_data/incidents.csv")
    exp = Exporter(generator, "generated_data")
    exp.export_all()

    end = time.time()
    print("Time exporting:", end - start)


if __name__ == "__main__":
    main()
