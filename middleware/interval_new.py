#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
import json
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Tuple
import pandas as pd
from IO.iowrapper import get_dataframe


@dataclass()
class Interval(ABC):
    """ Represents basic interval of an activity"""
    id: int = None
    activity_id: int = None
    name: str = None
    start: int = None
    end: int = None
    range: Tuple[int, int] = field(default_factory=tuple[int, int])

    def __pos_init__(self):
        self.range = self.start, self.end
        self.sort_index = self.id
        self.populate_metrics()

    def create(self, id, activity_id, name, start, end) -> Interval:
        """Return populated interval"""
        self.id = id
        self.activity_id = activity_id
        self.name = name
        self.start = start
        self.end = end
        self.range = self.start, self.end
        return self

    def dumps_to_json(self) -> str:
        return json.dumps(vars(self), indent=4, default=pd.DataFrame.to_csv)

    @abstractmethod
    def populate_metrics(self) -> None:
        """Compute and populate interval metrics"""


@dataclass()
class CyclingInterval(Interval):

    avg_power: int = 0
    max_power: int = 0
    min_power: int = 0

    avg_hr: int = 0
    max_hr: int = 0
    min_hr: int = 0

    avg_cad: int = 0
    max_cad: int = 0
    min_cad: int = 0

    def populate_metrics(self) -> None:
        df = get_dataframe(activity_id=self.activity_id).iloc[self.start:self.end]
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
