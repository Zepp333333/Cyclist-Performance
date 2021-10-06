#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from __future__ import annotations

import json
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import pandas as pd

from .interval import Interval
from .interval_factory import IntervalFactory
from .interval_finder import IntervalFinder


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
    interval_finder: IntervalFinder
    id: int
    name: str
    athlete_id: int
    date: datetime
    dataframe: pd.DataFrame
    details: dict
    intervals: list[Interval] = field(default_factory=list[Interval])
    type: str = 'Ride'

    def __post_init__(self) -> None:
        if not self.dataframe.empty:
            self.make_all_activity_interval()

    def make_all_activity_interval(self) -> None:
        if 'All' not in [n.name for n in self.intervals]:
            self.add_interval(
                name='All',
                start=0,
                end=int(self.dataframe.last_valid_index() or 0)
            )

    def add_interval(self, start: int, end: int, name: str = None) -> None:
        # todo: add code to check correctness of interval range
        if not name:
            name = self._generate_interval_name()
        self.add_intervals([self._make_interval(start, end, name)])

    def add_intervals(self, new_intervals: list[Interval]) -> None:
        for interval in new_intervals:
            if interval.name not in [n.name for n in self.intervals]:
                self.intervals.append(interval)

    def _make_interval(self, start: int, end: int, name: str = None) -> Interval:
        # todo: add code to check correctness of interval range
        interval = self.interval_factory.get_interval()
        return interval.create(id=len(self.intervals),
                               activity_id=self.id,
                               name=name,
                               start=start,
                               end=end,
                               dataframe=self.dataframe)

    def _generate_interval_name(self) -> str:
        proposed_name = f"Interval {len(self.intervals)}"
        return proposed_name

    def remove_intervals(self, intervals_to_remove: list[Interval]) -> None:
        for interval in intervals_to_remove:
            if interval not in self.intervals:
                raise IntervalDoNotExit(name=interval.name,
                                        id=interval.id,
                                        message="Interval doesn't exist in list of intervals.")
            self.intervals.remove(interval)

    def find_intervals(self, duration: int, count: int, power: int, tolerance: float) -> list[Interval]:
        found = self.interval_finder.find_manual(duration=duration,
                                                 count=count,
                                                 tolerance=tolerance,
                                                 dataframe=self.dataframe.watts,
                                                 power=power)
        intervals = []
        i = 1
        for interval in found:
            intervals.append(self._make_interval(interval[0], interval[1], f'{duration}-sec interval {i}'))
            i += 1
        return intervals

    def delete_intervals(self) -> None:
        self.intervals = []
        self.make_all_activity_interval()

    def intervals_to_json(self) -> list[str]:
        return [i.to_json() for i in self.intervals]

    @classmethod
    def read_intervals_from_json(cls, lst: list[str]) -> list[Interval]:
        return [Interval.from_json(s) for s in lst]

    def details_to_json(self) -> str:
        def _details_encoder(obj: Any):
            if isinstance(obj, datetime):
                return {
                    "_type": "datetime",
                    "value": obj.isoformat()
                }
            return obj

        return json.dumps(self.details, default=_details_encoder, indent=4)

    @classmethod
    def read_details_from_json(cls, string: str) -> dict:
        def _details_decoder(obj: Any):
            if "_type" in obj:
                if obj['_type'] == 'datetime':
                    return datetime.fromisoformat(obj['value'])
            return obj

        return json.loads(string, object_hook=_details_decoder)


@dataclass
class CyclingActivity(Activity):
    """Represents Cycling Activity"""
    type: str = 'Ride'


@dataclass
class RunningActivity(Activity):
    """Represents Running Activity"""
    type: str = 'Run'
