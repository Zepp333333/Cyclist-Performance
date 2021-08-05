#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import json
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Tuple
import pandas as pd


class Interval(ABC):
    """ Represents basic interval of an activity"""
    id: int
    name: str
    start: int
    end: int
    df: pd.DataFrame
    range: Tuple[int, int] = field(default_factory=tuple)

    def __pos_init__(self):
        self.sort_index = self.id
        self.populate_metrics(self.df.iloc[self.start:self.end])

    def dumps_to_json(self) -> str:
        return json.dumps(vars(self), indent=4)

    @abstractmethod
    def populate_metrics(self, df: pd.DataFrame) -> None:
        """Compute and populate interval metrics"""


@dataclass
class CyclingInterval(Interval):



    def __init__(self, args, kwargs):
        super().__init__(id, name, start, end, df)

        self.avg_power: int = 0
        self.max_power: int = 0
        self.min_power: int = 0

        self.avg_hr: int = 0
        self.max_hr: int = 0
        self.min_hr: int = 0

        self.avg_cad: int = 0
        self.max_cad: int = 0
        self.min_cad: int = 0

        self.populate_metrics(df.iloc[self.start:self.end])

    def populate_metrics(self, df: pd.DataFrame) -> None:
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

