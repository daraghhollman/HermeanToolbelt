import datetime as dt
import pickle

import matplotlib.pyplot as plt
import pandas as pd


def Load_Crossings(path: str) -> pd.DataFrame:
    """Loads a pandas DataFrame from pickle file.

    Parameters
    ----------
    path : str
        An abosolute path to a crossing intervals file.
        Expects the following columns to be present in the
        pickle file:
            [start,
             end,
             start_x_msm, end_x_msm,
             start_y_msm, end_y_msm,
             start_z_msm, end_z_msm,
             Type
            ]


    Returns
    -------
    Crossings Data : pandas.DataFrame
        A DataFrame of boundary crossing intervals with columns:
            [start,
             end,
             start_x_msm, end_x_msm,
             start_y_msm, end_y_msm,
             start_z_msm, end_z_msm,
             type
            ]
    """
    with open(path, "rb") as crossings_file:
        crossings_data = pickle.load(crossings_file)

    reformatted_crossings_data = pd.DataFrame(
        {
            "start": crossings_data["start"],
            "end": crossings_data["end"],
            "start_x_msm": crossings_data["start_x_msm"],
            "start_y_msm": crossings_data["start_y_msm"],
            "start_z_msm": crossings_data["start_z_msm"],
            "type": crossings_data["Type"],
        }
    )

    return reformatted_crossings_data


def Plot_Crossing_Intervals(
    ax: plt.Axes,
    start: dt.datetime,
    end: dt.datetime,
    crossings: pd.DataFrame,
    label: bool = True,
    color: str = "orange",
) -> None:
    """Adds vertical lines marking the start and end of given
    crossing intervals.

    Detects crossing intervals present in range of data.
    Vertical lines in the form of pyplot.axvlines() are added
    to a pyplot.Axes object `ax`, with optional labelling of
    type.

    Parameters
    ---------
    ax : pyplot.Axes
        The pyplot axis to add the vertical lines to.

    start : datetime.datetime
        The starting point of the data plotted.

    end : datetime.datetime
        The ending point of the data plotted.

    crossings : pandas.DataFrame
        A pandas DataFrame with crossings data, as generated by
        Load_Crossings().

    label : bool {`True`, `False`}
        If `True`, adds a label specificing the boundary type.

    color : str {`orange`, any other matplotlib named colour}


    Returns
    -------
    None
    """

    for _, row in crossings.iterrows():

        # If crossing interval is in plot
        if (row["start"] > start and row["start"] < end) or (
            row["end"] > start and row["end"] < end
        ):
            midpoint = row["start"] + (row["end"] - row["start"]) / 2

            if label:
                height: float = 0.9
                ax.text(
                    (midpoint - start).total_seconds() / (end - start).total_seconds(),
                    height,
                    row["type"].upper().replace("_", " "),
                    transform=ax.transAxes,
                    color=color,
                    ha="center",
                    va="center",
                )

            ax.axvline(row["start"], color=color, ls="dashed")
            ax.axvline(row["end"], color=color, ls="dashed")


def Plot_Crossings_As_Minutes_Before(
    ax: plt.Axes,
    crossings: pd.DataFrame,
    data_start: dt.datetime,
    data_end: dt.datetime,
    apoapsis_time: dt.datetime,
    label: bool = True,
    height: float = 0.9,
    color: str = "orange",
) -> None:
    """
    Plots crossings as vlines with respect to the closest
    apoapsis.

    Detects crossing intervals present in range of data.
    Vertical lines in the form of pyplot.axvlines() are added
    to a pyplot.Axes object `ax`, with optional labelling of
    type. A reference `apoapsis_time` is used to convert to
    minutes before apoapsis instead of a date.

    Parameters
    ---------
    ax : pyplot.Axes
        The pyplot axis to add the vertical lines to.

    crossings : pandas.DataFrame
        A pandas DataFrame with crossings data, as generated by
        Load_Crossings().

    data_start : datetime.datetime
        The starting point of the data plotted.

    data_end : datetime.datetime
        The ending point of the data plotted.

    apoapsis_time : datetime.datetime
        The time of the reference apoapsis.

    label : bool {`True`, `False`}
        If `True`, adds a label specificing the boundary type.

    height : float {`0.9`}, optional
        The height of the label in axis units.

    color : str {`orange`, any other matplotlib named colour}, optional
        The colour of the vertical lines and labels.


    Returns
    -------
    None
    """

    for _, row in crossings.iterrows():

        # Check if crossing interval is in plot
        if (row["start"] > data_start and row["start"] < data_end) or (
            row["end"] > data_start and row["end"] < data_end
        ):

            midpoint = row["start"] + (row["end"] - row["start"]) / 2

            # Convert times into minutes before apoapsis
            start_minutes = (apoapsis_time - row["start"]).total_seconds() / 60
            end_minutes = (apoapsis_time - row["end"]).total_seconds() / 60

            if label:
                ax.text(
                    (midpoint - data_start).total_seconds()
                    / (data_end - data_start).total_seconds(),
                    height,
                    row["type"].upper().replace("_", " "),
                    transform=ax.transAxes,
                    color=color,
                    ha="center",
                    va="center",
                )

            ax.axvline(start_minutes, color=color, ls="dashed")
            ax.axvline(end_minutes, color=color, ls="dashed")
