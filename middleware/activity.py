#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pandas as pd
from middleware import Interval
from IO import DataWrapper


class Activity:
    def __init__(self,
                 name: str,
                 df: pd.DataFrame,
                 intervals: list[Interval] = None,
                 activity_type: str = 'Bike'
                 ):
        if intervals is None:
            intervals = []
        self.name = name
        self.df = df
        self.intervals = intervals
        self.activity_type = activity_type

        self.all_activity = Interval(activity=self,
                                     title="all activity",
                                     start=0,
                                     end=df.last_valid_index())
        self.add_intervals([self.all_activity])

    def add_intervals(self, new_intervals: list[Interval]) -> None:
        self.intervals.extend(new_intervals)

    def make_interval(self, start, end):
        # todo: add code to check correctness of interval range
        new_interval = Interval(activity=self,
                                title=f"Interval {len(self.intervals)}",
                                start=start,
                                end=end)
        self.add_intervals([new_interval])

    def remove_intervals(self, intervals: list[Interval]) -> None:
        for interval in intervals:
            try:
                self.intervals.remove(interval)
            except ValueError:
                # Todo replace with logging
                print(f"Interval {interval} not in list of intervals for activity {self.name}")

    def check_if_interval_exit(self, interval_to_check: Interval) -> bool:
        return interval_to_check in self.intervals



# dw = DataWrapper()
# df = dw.get_activity(activity_id='ride.csv')
#
# a = Activity('test-ride', df)
#
#
# print('A interval = ', a.intervals)
# b = Activity('test-ride2', df)
# print('B interval = ', b.intervals)