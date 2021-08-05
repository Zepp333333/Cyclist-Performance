#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class IntervalDoNotExit(Exception):
    """Custom error in case accessing non-existent interval"""
    def __init__(self, name: str, id: int, message: str) -> None:
        self.name = name
        self.id = id
        self.message = message
        super().__init__(message)


@dataclass
class Activity(ABC):
    """Represents basic activity"""
    name: str
    id: str
    type: str
    intervals: List[Interval] = field(default_factory=list)
    df: pd.DataFrame = None

    def __post_init__(self):
        self.intervals: List[Interval] =

    def add_intervals(self, new_intervals: List[Interval]) -> None:
        self.intervals.extend(new_intervals)

    def remove_intervals(self, intervals_to_remove: List[Interval]) -> None:
        for interval in intervals_to_remove:
            if interval not in self.intervals:
                raise IntervalDoNotExit(name=interval.name,
                                        id=interval.id,
                                        message="Interval doesn't exist in list of intervals.")
            self.intervals.remove(interval)

    def check_if_interval_exit(self, interval_to_check: Interval) -> bool:
        return interval_to_check in self.intervals

