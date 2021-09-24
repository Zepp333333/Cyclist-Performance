#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pandas as pd
from logic import Activity

DEFAULT_DURATIONS = [
        *range(1, 61),
        *range(65, 121, 5),
        *range(130, 310, 10),
        *range(330, 630, 30),
        *range(660, 3660, 60),
        *range(3900, 43500, 300)
    ]


def calculate_cp(activity: Activity) -> tuple[pd.DataFrame, str]:
    methods = {
        'Ride': calculate_ride_cp,
        'VirtualRide': calculate_ride_cp,
        'Run': calculate_run_cp,
    }
    method = methods[activity.type]
    return method(activity.dataframe)


def calculate_ride_cp(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Takes a ride activity df and produce dataframe containing Critical Power (alt called Power-Duration) dataset for predefined set of durations"""
    metric_series_name = 'watts'
    return _calculate_metric_duration_chart(df=df, metric_series_name=metric_series_name), metric_series_name


def calculate_run_cp(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Takes a run activity df and produce dataframe containing Critical Pace (alt called Pace-Duration) dataset for predefined set of durations"""
    metric_series_name = 'pace'
    return _calculate_metric_duration_chart(df=df, metric_series_name=metric_series_name), metric_series_name


def _calculate_metric_duration_chart(df: pd.DataFrame,
                                     metric_series_name: str,
                                     time_series_name: str = 'time',) -> pd.DataFrame:
    durations = []
    metric_series = []
    last_record = df[time_series_name].max()

    for d in DEFAULT_DURATIONS:
        if d > last_record:
            break
        durations.append(d)
        metric_series.append(df[metric_series_name].rolling(d).mean().max())

        # alternative approach - full-resolution CP curve:
        # pd = [df['watts'].rolling(d).mean().max() for d in range(len(df['time']))]

    cp = pd.DataFrame().reindex(columns=[time_series_name, metric_series_name])
    cp[time_series_name] = durations
    cp[metric_series_name] = metric_series
    return cp


def calculate_list_of_rides_cp(activities: list[Activity]) -> pd.DataFrame:
    """Takes a list of Activities and produce dataframe containing Critical Power (alt called Power-Duration) dataset:
        Duration-Max(Avg(Power) for predefined set of durations"""

    cons_power = pd.DataFrame().reindex(columns=['Duration'])
    for activity in activities:
        cp = calculate_ride_cp(activity.dataframe)
        cons_power[activity.id] = cp['Watts']

    return cons_power


# test code

# from iobrocker import IO
# from datetime import datetime
#
# with app.app_context():
#     io = IO(1)
#     l = io.get_list_of_activities_in_range(datetime(2021, 8, 1), datetime(2021, 8, 30))
#
# activities = []
# with app.app_context():
#     for pa in l:
#         activities.append(io.get_hardio_activity_by_id(pa.id))

# cons_power['Duration'] = DEFAULT_DURATIONS[0:len(cons_power.index)]
# cons_power['cp'] = cons_power.max(axis=1)
