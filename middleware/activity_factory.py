#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
from abc import ABC, abstractmethod
from activity_new import Activity, CyclingActivity
from interval_new import Interval, CyclingInterval


class ActivityFactory(ABC):
    """Factory that represents combination of Activity an Interval.
    Doesn't maintain any of the instances it creates"""

    @abstractmethod
    def get_activity(self, *args, **kwargs) -> Activity:
        """Returns activity belonging to this factory"""

    @abstractmethod
    def get_interval(self) -> Interval:
        """Returns interval belonging to this factory"""


class BikeActivityFactory(ActivityFactory):
    def get_activity(self, **kwargs) -> Activity:
        return CyclingActivity(**kwargs, interval=self.get_interval())

    def get_interval(self):
        return CyclingInterval()

