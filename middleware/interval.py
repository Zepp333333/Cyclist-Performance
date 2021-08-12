#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
import pandas as pd
import pickle


@dataclass()
class Interval(ABC):
    """ Represents basic interval of an activity
        Use Interval.create method to populate factory instantiated instances"""
    id: int = None
    activity_id: int = None
    name: str = None
    start: int = None
    end: int = None
    dataframe: pd.DataFrame = pd.DataFrame()

    def __post_init__(self) -> None:
        """Populate post-init fields and metrics"""
        self.sort_index = self.id
        self.populate_metrics(self.dataframe)
        del self.dataframe

    def create(self, id, activity_id, name, start, end, dataframe) -> Interval:
        """Return populated interval. Use for factory instantiated instances"""
        self.id = id
        self.activity_id = activity_id
        self.name = name
        self.start = start
        self.end = end
        self.populate_metrics(dataframe)
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

    def pickle(self):
        return pickle.dumps(self)

    @classmethod
    def from_pickle(cls, pickle_str):
        return pickle.loads(pickle_str)


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
        df = dataframe.iloc[self.start:self.end]
        if 'watts' in df:
            self.populate_watts(df)
        if 'heartrate' in df:
            self.populate_hr(df)
        if 'cadence' in df:
            self.populate_cad(df)

    def populate_watts(self, df) -> None:
        self.avg_power = df.watts.mean()
        self.max_power = df.watts.max()
        self.min_power = df.watts.min()

    def populate_hr(self, df) -> None:
        self.avg_hr = df.heartrate.mean()
        self.max_hr = df.heartrate.max()
        self.min_hr = df.heartrate.min()

    def populate_cad(self, df) -> None:
        self.avg_cad = df.cadence.mean()
        self.max_cad = df.cadence.max()
        self.min_cad = df.cadence.min()

#todo remove testing code
# df = pd.read_csv('../iobrocker/ride.csv')
# c = CyclingInterval(id=1, activity_id=1, name='something', start=250, end=2500, dataframe=df)
