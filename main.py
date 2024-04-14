import random
from datetime import datetime

import numpy as np
from exporter import Exporter
from generator import Generator
from utils.constants import INITIAL_COUNTS


def main():
    SEED = 42
    np.random.seed(SEED)
    random.seed(SEED)

    startdate = datetime(2023, 1, 1)
    enddate = datetime(2023, 1, 31)

    generator = Generator(INITIAL_COUNTS, startdate, 600, 16)
    generator.generate_initial_data()

    generator.assign_teams()

    generator.simulate(startdate, enddate)

    exp = Exporter(generator, "generated_data", False)
    exp.export_all()


if __name__ == "__main__":
    main()
