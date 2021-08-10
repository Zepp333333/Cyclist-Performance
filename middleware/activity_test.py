#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import json
import pandas as pd
from sqlalchemy.orm import reconstructor

from cycperf.models import DBActivity
from .interval_new import Interval


class Activity(DBActivity):
    @reconstructor
    def init_on_load(self):
        print('running reconstructor' )
        if not self.intervals:
            print("self.intervals = ", self.intervals)
            self.intervals = []
            print("self.intervals = ", self.intervals)
            whole_activity = Interval(activity_id=self.activity_id,
                                      df=self.df,
                                      name="all activity",
                                      start=0,
                                      end=self.df.last_valid_index())
            print(whole_activity)
            self.add_intervals([whole_activity])
            print("self.intervals = ", self.intervals)
        print('finished reconstructor')

    @property
    def df(self):
        return pd.read_json(self.df_json)

    @property
    def name(self):
        return self.json['name']

    @property
    def type(self):
        return self.json['type']

    def add_intervals(self, new_intervals: list[Interval]) -> None:
        self.intervals.extend(new_intervals)

    def make_interval(self, start, end) -> Interval:
        # todo: add code to check correctness of interval range
        return Interval(activity_id=self.activity_id,
                        df=self.df,
                        name=f"Interval {len(self.intervals)}",
                        start=start,
                        end=end)

    def remove_intervals(self, intervals_to_remove: list[Interval]) -> None:
        for interval in intervals_to_remove:
            try:
                self.intervals.remove(interval)
            except ValueError:
                # Todo replace with logging
                print(f"Interval {interval} not in list of intervals for activity {self.name}")

    def check_if_interval_exit(self, interval_to_check: Interval) -> bool:
        return interval_to_check in self.intervals

    def __str__(self):
        return f"Activity: {self.activity_id}, {self.name}"
