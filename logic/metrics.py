#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from __future__ import annotations

from typing import Optional

from logic import Activity
from logic.datafield_calculator import DataFieldCalculator, CALCULATORS, MEASURES


class Metric:
    """
    Defines interface for Activity Metric(s)
    implements Strategy pattern
    """

    def __init__(self, name: str, measure: str, strategy: DataFieldCalculator,
                 config: dict = None) -> None:
        self.name: str = name
        self.measure: str = measure
        self.strategy = strategy
        self.config = config

        self.value: Optional[float] = None

    def calculate(self, df: Activity.dataframe) -> None:
        """calculate data field and store it in self.value"""
        self.value = self.strategy(df, self.config)

    def __str__(self):
        return f"{self.name.title()}: {round(self.value)}{self.measure}"


class ActivityMetrics:
    """
    Represents a set of data fields of an Activity
    """
    def __init__(self, activity: Activity, config: dict = None) -> None:
        self.activity = activity
        self.config = config

    def populate(self) -> None:
        for name, strategy in CALCULATORS.items():
            measure = MEASURES[name] or ''
            field = Metric(name=name, strategy=strategy(), measure=measure, config=self.config)
            field.calculate(self.activity.dataframe)
            self.__setattr__(name, field)


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
#     RPE: int = None
#
#
#
#
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
