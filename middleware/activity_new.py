#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from __future__ import annotations

import pickle
from abc import ABC
from dataclasses import dataclass, field

import pandas as pd

from .interval_factory import IntervalFactory
from .interval_new import Interval


class IntervalDoNotExit(Exception):
    """Custom error in case accessing non-existent interval"""
    # todo consider moving to exceptions package
    def __init__(self, name: str, id: int, message: str) -> None:
        self.name = name
        self.id = id
        self.message = message
        super().__init__(message)


@dataclass
class Activity(ABC):
    """Represents basic activity interface"""
    interval_factory: IntervalFactory
    id: int
    name: str
    athlete_id: int
    dataframe: pd.DataFrame
    intervals: list[Interval] = field(default_factory=list[Interval])
    type: str = 'bike'

    def __post_init__(self) -> None:
        self.add_intervals([self.make_whole_activity_interval()])

    def make_whole_activity_interval(self) -> Interval:
        interval = self.interval_factory.get_interval()
        return interval.create(id=0,
                               activity_id=self.id,
                               name='Whole Activity',
                               start=0,
                               end=self.dataframe.last_valid_index(),
                               dataframe=self.dataframe)

    def new_interval(self, start: int, end: int, name: str = None) -> None:
        if not name:
            name = self.generate_interval_name()
        self.add_intervals([self.make_interval(start, end, name)])

    def add_intervals(self, new_intervals: list[Interval]) -> None:
        self.intervals.extend(new_intervals)

    def make_interval(self, start: int, end: int, name: str = None) -> Interval:

        interval = self.interval_factory.get_interval()
        return interval.create(id=len(self.intervals),
                               activity_id=self.id,
                               name=name,
                               start=start,
                               end=end,
                               dataframe=self.dataframe)

    def generate_interval_name(self) -> str:
        proposed_name = f"Interval {len(self.intervals)}"
        return proposed_name

    def remove_intervals(self, intervals_to_remove: list[Interval]) -> None:
        for interval in intervals_to_remove:
            if interval not in self.intervals:
                raise IntervalDoNotExit(name=interval.name,
                                        id=interval.id,
                                        message="Interval doesn't exist in list of intervals.")
            self.intervals.remove(interval)

    def check_if_interval_exit(self, interval_to_check: Interval) -> bool:
        return interval_to_check in self.intervals

    def pickle(self) -> bytes:
        return pickle.dumps(self, protocol=0)

    @classmethod
    def from_pickle(cls, pickle_str) -> Activity:
        return pickle.loads(pickle_str)


@dataclass
class CyclingActivity(Activity):
    """Represents Cycling Activity"""
