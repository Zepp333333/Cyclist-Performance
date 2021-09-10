#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

import json
from dataclasses import dataclass
from abc import ABC, abstractmethod
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
    # dataframe: pd.DataFrame = pd.DataFrame()

    # def __post_init__(self) -> None:
    #     """Populate post-init fields and metrics"""
    #     self.sort_index = self.id
    #     self.populate_metrics(self.dataframe)
    #     del self.dataframe

    def create(self, id, activity_id, name, start, end, dataframe) -> Interval:
        """Return populated interval. Use for factory instantiated instances"""
        self.id = id
        self.activity_id = activity_id
        self.name = name
        self.start = start
        self.end = end
        self.populate_metrics(dataframe)
        # del self.dataframe
        return self

    @abstractmethod
    def populate_metrics(self, dataframe: pd.DataFrame) -> None:
        """Compute and populate interval metrics"""

    def change_interval(self,
                        new_start: int, new_end: int,
                        dataframe: pd.DataFrame, new_name: str = None):
        """Changes interval range and name, initiates recalculation of metrics
        based on provided activity dataframe"""
        self.start, self.end = new_start, new_end
        if new_name:
            self.name = new_name
        self.populate_metrics(dataframe)

    def __eq__(self, other):
        return self.name == other.name or (self.start == other.start and self.end == other.end)


@dataclass()
class CyclingInterval(Interval):
    """ Represents basic interval of an activity
        Use Interval.create method to populate factory instantiated instances"""

    avg_power: int = 0
    max_power: int = 0
    min_power: int = 0

    avg_hr: int = 0
    max_hr: int = 0
    min_hr: int = 0

    avg_cad: int = 0
    max_cad: int = 0
    min_cad: int = 0

    def populate_metrics(self, dataframe: pd.DataFrame) -> None:
        """Compute and populate interval metrics"""
        df = dataframe.loc[(dataframe['time'] >= self.start) & (dataframe['time'] <= self.end)]
        if 'watts' in df:
            self.populate_watts(df)
        if 'heartrate' in df:
            self.populate_hr(df)
        if 'cadence' in df:
            self.populate_cad(df)

    def populate_watts(self, df: pd.DataFrame) -> None:
        self.avg_power = int(df.watts.mean())
        self.max_power = int(df.watts.max())
        self.min_power = int(df.watts.min())

    def populate_hr(self, df) -> None:
        self.avg_hr = int(df.heartrate.mean())
        self.max_hr = int(df.heartrate.max())
        self.min_hr = int(df.heartrate.min())

    def populate_cad(self, df) -> None:
        self.avg_cad = int(df.cadence.mean())
        self.max_cad = int(df.cadence.max())
        self.min_cad = int(df.cadence.min())


@dataclass()
class RunningInterval(Interval):
    avg_pace: int = 0
    max_pace: int = 0
    min_pace: int = 0

    avg_hr: int = 0
    max_hr: int = 0
    min_hr: int = 0

    def populate_metrics(self, dataframe: pd.DataFrame) -> None:
        """Compute and populate interval metrics"""
        df = dataframe.loc[(dataframe['time'] >= self.start) & (dataframe['time'] <= self.end)]
        if 'pace' in df:
            self.populate_pace(df)
        if 'heartrate' in df:
            self.populate_hr(df)

    def populate_pace(self, df: pd.DataFrame) -> None:
        self.avg_pace = int(df.pace.mean())
        self.max_pace = int(df.pace.max())
        self.min_pace = int(df.pace.min())

    def populate_hr(self, df) -> None:
        self.avg_hr = int(df.heartrate.mean())
        self.max_hr = int(df.heartrate.max())
        self.min_hr = int(df.heartrate.min())
