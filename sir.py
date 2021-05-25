# Imports
from typing import Iterator, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numba


def sir(
        susceptible: int,
        infected: int,
        recovered: int,
        beta: float,
        gamma: float = 1 / 14,
        case_adjustment_factor: float = 10,
        start: int = 0,
        stop: int = 90
) -> Iterator[Tuple[
    int,
    float,
    float,
    float,
]]:
    """
    Calculate the number of susceptible people and incidence and prevalence
    of infection and recovery in a population based on initial values.

    Core SIR model function that forecasts new
    - susceptible (S),
    - infected (I), and
    - recovered (R) values

    Arguments:
        susceptible: Initial number of susceptible people.
        infected: Initial number of total confirmed infections.
        recovered: Initial number of people who have recovered.
        beta: The effective contact rate during social distancing.
            BETA = (GROWTH_RATE + GAMMA) / SUSCEPTIBLE
        gamma: The inverse of the recovery length, e.g.
            RECOVERY_TIME = 7
            GAMMA = 1 / RECOVERY_TIME
        case_adjustment_factor: A multiplier to estimate the true case count.
            Under-reporting of cases is common because many are asymptomatic.
            The case adjustment factor compensates for under-reporting.
        start: The day for which initial values are provided, e.g. day 0.
        stop: The total number of days to forecast (daily projections).

    Yields:
        Collected values across each day from start to end.
        1. day
        2. susceptible
        3. total infected (infected prevalence)
        4. total recovered (recovered prevalence)
    """
    # Iterate over days and yield model outputs
    for day in range(start, stop + 1):
        yield (
            day,
            susceptible,
            infected,
            recovered,
        )
        # New confirmed infections (new positive tests)
        infected_incidence = beta * infected * susceptible
        # Number of infected who have just recovered
        recovered_incidence = gamma * infected
        # Number of people who are susceptible as of this time point
        susceptible_new = (
                susceptible
                - case_adjustment_factor
                * infected_incidence
        )
        # Total number of people who are infected as of this time point
        infected_prevalence = (
                infected_incidence
                + infected
                - recovered_incidence
        )
        # Total number of people who have recovered as of this time point
        recovered_prevalence = (
                recovered_incidence
                + recovered
                + infected_incidence * max(1., case_adjustment_factor - 1)
        )
        # Overwrite initial values with current values
        susceptible, infected, recovered = (
            susceptible_new, infected_prevalence, recovered_prevalence
        )


def random_sir(
        susceptible: int,
        infected: int,
        recovered: int,
        beta: float = None,
        betas: Iterator[float] = None,
        gamma: float = 1 / 7,
        case_adjustment_factor: float = 10,
        start: int = 0,
        stop: int = 90
) -> Iterator[Tuple[
    int,
    int,
    int,
    int,
]]:
    """
    Calculate the number of susceptible people and incidence and prevalence
    of infection and recovery in a population based on initial values.

    Core SIR model function that forecasts new
    - susceptible (S),
    - infected (I), and
    - recovered (R) values

    Arguments:
        susceptible: Initial number of susceptible people.
        infected: Initial number of total confirmed infections.
        recovered: Initial number of people who have recovered.
        beta: The effective contact rate during social distancing.
            BETA = (GROWTH_RATE + GAMMA) / SUSCEPTIBLE
        betas: A generator that provides beta values.
        gamma: The inverse of the recovery length, e.g.
            RECOVERY_TIME = 7
            GAMMA = 1 / RECOVERY_TIME
        case_adjustment_factor: A multiplier to estimate the true case count.
            Under-reporting of cases is common because many are asymptomatic.
            The case adjustment factor compensates for under-reporting.
        start: The day for which initial values are provided, e.g. day 0.
        stop: The total number of days to forecast (daily projections).

    Yields:
        Collected values across each day from start to end.
        1. day
        2. susceptible
        3. total infected (infected prevalence)
        4. total recovered (recovered prevalence)
    """
    # Iterate over days and yield model outputs
    for day in range(start, stop + 1):
        yield (
            day,
            susceptible,
            infected,
            recovered,
        )
        if betas is None and beta is None:
            raise ValueError("You must provide beta and/or betas.")
        # Get b from betas but use beta as a default beta
        elif betas is not None and beta is not None:
            b = next(betas, beta)
        # Get b from betas but use zero as a default beta
        elif betas is not None:
            b = next(betas, 0)
        # Get b from beta
        else:
            b = beta
        # Calculate probability of becoming infected
        prob = b * infected / susceptible
        # If probability is nan, inf, greater than one, or less than zero,
        if np.isinf(prob) or np.isnan(prob) or prob > 1 or prob < 0:
            # set probability to zero
            prob = 0
        # New confirmed infections (new positive tests)
        infected_incidence = np.random.binomial(
            susceptible,
            prob,
            susceptible
        ).sum()
        # Number of infected who have just recovered
        recovered_incidence = int(round(gamma * infected, 0))
        # Number of people who are susceptible as of this time point
        susceptible_new = max(
            susceptible - case_adjustment_factor * infected_incidence,
            0
        )
        # Total number of people who are infected as of this time point
        infected_prevalence = max(
            infected_incidence + infected - recovered_incidence,
            0
        )
        # Total number of people who have recovered as of this time point
        recovered_prevalence = max(
            recovered_incidence + recovered
            + infected_incidence * max(1., case_adjustment_factor - 1),
            0
        )
        # Overwrite initial values with current values
        susceptible, infected, recovered = (
            susceptible_new, infected_prevalence, recovered_prevalence
        )


if __name__ == '__main__':
    columns = [
        "day",
        "susceptible",
        "infected",
        "recovered"
    ]

    df = pd.DataFrame(
        sir(
            susceptible=100000,
            infected=300,
            recovered=0,
            beta=2e-6,
        ),
        columns=columns)

    random_df = pd.DataFrame(
        random_sir(
            susceptible=100000,
            infected=300,
            recovered=0,
            beta=2e-6,
        ),
        columns=columns)

    df.plot.line(y=columns[1:])
    random_df.plot.line(y=columns[1:])
    plt.show()

    # Compare s, i, and r obtained from two betas
    random_arr = np.concatenate([
        tuple(
            random_sir(
                susceptible=100000,
                infected=300,
                recovered=0,
                beta=beta,
            )
        ) for beta in [2e-6, 3e-6]
    ],
        axis=1
    )
    s = random_arr[:, 1::4]
    i = random_arr[:, 2::4]
    r = random_arr[:, 3::4]

