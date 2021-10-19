#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from __future__ import annotations

from typing import Optional

from logic import Activity
from logic.metric_calculator import MetricCalculator, CALCULATORS, MEASURES


class Metric:
    """
    Defines interface for Activity Metric(s)
    implements Strategy pattern
    """

    def __init__(self, name: str, measure: str, strategy: MetricCalculator,
                 config: dict = None) -> None:
        self.name: str = name
        self.measure: str = measure
        self.strategy: MetricCalculator = strategy
        self.config: dict = config
        self.title: str = ''

        self.value: Optional[float] = None

    def calculate(self, df: Activity.dataframe) -> None:
        """calculate data field and store it in self.value"""
        self.value, self.title = self.strategy(df, self.config)

    def __str__(self):
        return f"{self.title}: {round(self.value)}{self.measure}"


class ActivityMetrics:
    """
    Represents a set of Metrics of an Activity
    """
    def __init__(self, activity: Activity, config: dict) -> None:
        self.activity = activity
        self.config = config

        self.load = None
        self.intensity = None
        self.average_power = None
        self.normalized = None
        self.average_hr = None
        self.max_hr = None
        self.average_cad = None
        self.work = None

        if self.activity.type == ("VirtualRide" or "Ride"):
            self.populate()

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
