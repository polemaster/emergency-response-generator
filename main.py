import random

import numpy as np
from exporter import Exporter
from generator import Generator
from utils.constants import (
    INCIDENTS_PER_HOUR,
    INITIAL_COUNTS,
    NUMBER_OF_TUPLES,
    SEED,
    SIMULATION_TIMESTEP,
    START_DATE,
)


def main():
    np.random.seed(SEED)
    random.seed(SEED)

    startdate = START_DATE

    generator = Generator(
        INITIAL_COUNTS, startdate, SIMULATION_TIMESTEP, INCIDENTS_PER_HOUR
    )
    generator.generate_initial_data()

    generator.assign_teams()

    generator.simulate(startdate, NUMBER_OF_TUPLES)

    exp = Exporter(generator, "generated_data", False)
    exp.export_all()


if __name__ == "__main__":
    main()
