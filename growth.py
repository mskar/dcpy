import numpy as np
import pandas as pd


def get_growth_rate(
    df: pd.DataFrame, time_col: str, case_col: str, window: int = 1
) -> pd.Series:
    """
    Args:
        df: The input dataframe.
        time_col: The name of the time column.
        case_col: The name of the case column.
        window: The window across which to calculate growth rate.

    Returns:
        A pandas Series containing the growth rate at each timestep.

    Examples:
        >>> df = pd.DataFrame({"x": range(3), "y": range(3, 6)})
        >>> get_growth_rate(df, "x", "y", 1)
        0         NaN
        1    0.333333
        2    0.250000
        dtype: float64
    """
    # End time (time point 2) - Start time (time point 1)
    time_differences = df[time_col].diff(window)
    try:
        return df[case_col].pct_change(window) / time_differences
    except ZeroDivisionError:
        return np.nan


def get_growth_rate_by_group(
    df: pd.DataFrame,
    group_col: str,
    time_col: str,
    case_col: str,
    window: int = 1,
) -> pd.Series:
    """
    Args:
        df: The input dataframe.
        time_col: The name of the grouping column.
        time_col: The name of the time column.
        case_col: The name of the case column.
        window: The window across which to calculate growth rate.

    Returns:
        A pandas Series containing the growth rate at each timestep.
    """
    # End time (time point 2) - Start time (time point 1)
    time_differences = df.groupby(group_col)[time_col].diff(window)
    # End value divided by Start value
    r = df.groupby(group_col)[case_col].pct_change(window)
    try:
        return r / time_differences
    except ZeroDivisionError:
        return np.nan


def get_doubling_time(df: pd.DataFrame, gr_col: str,) -> pd.Series:
    try:
        return np.log(2) / np.log(df[gr_col] + 1)
    except ZeroDivisionError:
        return np.nan


def get_beta(
    df: pd.DataFrame, gr_col: str, gamma: float, susceptible_col: str
) -> pd.Series:
    try:
        return (df[gr_col] + gamma) / df[susceptible_col]
    except ZeroDivisionError:
        return np.nan


def get_rt(
    df: pd.DataFrame, beta_col: str, gamma: float, susceptible_col: str
) -> pd.Series:
    try:
        return df[beta_col] / gamma * df[susceptible_col]
    except ZeroDivisionError:
        return np.nan
