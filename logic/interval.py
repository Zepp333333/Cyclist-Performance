#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

import json
from typing import Any

from datetime import datetime

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd


@dataclass()
class Interval(ABC):
    """ Represents basic interval of an activity
        Use Interval.create method to populate factory instantiated instances"""
    id: int = None
    activity_id: int = None
    name: str = None
    start: int = None
    end: int = None

    # General metrics which are expected to be present in any activity type
    avg_hr: int = 0
    max_hr: int = 0
    min_hr: int = 0

    avg_cad: int = 0
    max_cad: int = 0
    min_cad: int = 0

    def create(self, id, activity_id, name, start, end, dataframe) -> Interval:
        """Return populated interval. Use for factory instantiated instances"""
        self.id = id
        self.activity_id = activity_id
        self.name = name
        self.start = start
        self.end = end
        # self.populate_metrics(dataframe)
        return self

    def populate_metrics(self, dataframe: pd.DataFrame) -> None:
        if dataframe.empty:
            return
        dataframe_slice = dataframe.loc[(dataframe['time'] >= self.start) & (dataframe['time'] <= self.end)]
        self.populate_general_metrics(dataframe_slice)
        self.populate_specific_metrics(dataframe_slice)

    def populate_general_metrics(self, dataframe_slice) -> None:
        if 'heartrate' in dataframe_slice:
            self.populate_hr(dataframe_slice)
        if 'cadence' in dataframe_slice:
            self.populate_cad(dataframe_slice)

    @abstractmethod
    def populate_specific_metrics(self, dataframe_slice: pd.DataFrame) -> None:
        """Compute and populate interval metrics"""

    # todo need to check if actual mean, max and min are non Nan
    def populate_hr(self, df) -> None:
        self.avg_hr = int(df.heartrate.mean())
        self.max_hr = int(df.heartrate.max())
        self.min_hr = int(df.heartrate.min())

    def populate_cad(self, df) -> None:
        self.avg_cad = int(df.cadence.mean())
        self.max_cad = int(df.cadence.max())
        self.min_cad = int(df.cadence.min())

    def change_interval(self,
                        new_start: int, new_end: int,
                        dataframe: pd.DataFrame, new_name: str = None):
        """Changes interval range and name, initiates recalculation of metrics
        based on provided activity dataframe"""
        self.start, self.end = new_start, new_end
        if new_name:
            self.name = new_name
        self.populate_metrics(dataframe)

    @property
    def start_timestamp(self) -> datetime:
        return pd.to_datetime(self.start, unit='s')

    @property
    def end_timestamp(self) -> datetime:
        return pd.to_datetime(self.end, unit='s')

    def __eq__(self, other):
        return self.name == other.name or (self.start == other.start and self.end == other.end)

    def to_json(self) -> str:
        def _interval_encoder(obj: Any) -> Any:
            if isinstance(obj, Interval):
                return {
                    "_type": obj.__class__.__name__,
                    "value": obj.__dict__
                }
            return json.JSONEncoder().default(obj)
        return json.dumps(self, default=_interval_encoder, indent=4)

    @classmethod
    def from_json(cls, string) -> Interval:
        def _object_hook(obj):
            if '_type' in obj:
                if obj['_type'] == 'CyclingInterval':
                    return CyclingInterval(**obj['value'])
                if obj['_type'] == 'RunningInterval':
                    return RunningInterval(**obj['value'])
            if 'data' in obj:
                return obj['data']
            return obj
        return json.loads(string, object_hook=_object_hook)


@dataclass()
class CyclingInterval(Interval):
    """ Represents basic interval of an activity
        Use Interval.create method to populate factory instantiated instances"""

    avg_power: int = 0
    max_power: int = 0
    min_power: int = 0

    def populate_specific_metrics(self, dataframe_slice: pd.DataFrame) -> None:
        """Compute and populate interval metrics"""
        if 'watts' in dataframe_slice:
            self.populate_watts(dataframe_slice)

    def populate_watts(self, df: pd.DataFrame) -> None:
        self.avg_power = int(df.watts.mean())
        self.max_power = int(df.watts.max())
        self.min_power = int(df.watts.min())


@dataclass()
class RunningInterval(Interval):
    avg_pace: int = 0
    max_pace: int = 0
    min_pace: int = 0

    def populate_specific_metrics(self, dataframe_slice: pd.DataFrame) -> None:
        """Compute and populate interval metrics"""
        if 'pace' in dataframe_slice:
            self.populate_pace(dataframe_slice)
        if 'heartrate' in dataframe_slice:
            self.populate_hr(dataframe_slice)

    def populate_pace(self, df: pd.DataFrame) -> None:
        self.avg_pace = int(df.pace.mean())
        self.max_pace = int(df.pace.max())
        self.min_pace = int(df.pace.min())
