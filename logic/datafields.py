#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from __future__ import annotations

from typing import Optional

from logic import Activity
from logic.datafield_strategies import DataFieldStrategy
import logic.datafield_strategies as dss

class DataField:
    """
    DataField defines interface for Activity DataField(s)
    implements Strategy pattern
    """

    def __init__(self, name: str, measure: str, strategy: DataFieldStrategy,
                 config: dict = None) -> None:
        self.name: str = name
        self.measure: str = measure
        self.strategy = strategy
        self.config = config

        self.value: Optional[float] = None

    def calculate(self, df: Activity.dataframe) -> None:
        """calculate data field and store it in self.value"""
        self.value = self.strategy.calculate(df, self.config)

    def __str__(self):
        return f"{self.name.title()}: {round(self.value)}{self.measure}"


class ActivityFields:
    STRATEGIES = {
        'load': dss.Load,
        'intensity': dss.Intensity,
        'average power': dss.AveragePower,
        'normalized': dss.Normalized,
    }

    MEASURES = {
        'load': '',
        'intensity': '',
        'average power': 'wt',
        'normalized': 'wt',
    }

    def __init__(self, activity: Activity, config: dict = None) -> None:
        self.activity = activity
        self.config = config
        self.fields: dict = {}

    def populate(self) -> None:
        for name, strategy in self.STRATEGIES.items():
            measure = self.MEASURES[name] or ''
            field = DataField(name=name, strategy=strategy(), measure=measure, config=self.config)
            field.calculate(self.activity.dataframe)
            self.fields[name] = field




#     def __init__(self) -> None:
#     date: datetime = None
#     name: str = None
#     duration: float = None
#
#     time_moving: float = None
#     distance: float = None
#     elevation_gain: float = None
#     average_speed: float = None
#     sport: str = None
#
#     notes: str = None
#     keyword: str = None
#
#     TSS: float = None
#     IF: float = None
#     RPE: int = None
#
#     average_hr: float = None
#     max_hr: float = None
#     average_cad: float = None
#
#     NP: float = None
#     average_power: float = None
#     VI: float = None
#     Power_HR: float = None
#     LRBalance: float = None
#
#     device: str = None
#     recording_interval: int = None
#
#     weight: float = None
#     work: float = None
#     Work_above_FTP: float = None
#     Efficiency: float = None
#     FTP: float = None
#
#     def calculate_fields(self, fields_to_calculate: list[str]):
#         pass
