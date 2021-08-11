#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
from abc import ABC, abstractmethod
from .activity_new import Activity, CyclingActivity
from .interval_factory import IntervalFactory, CyclingIntervalFactory


class ActivityFactory(ABC):
    """Factory that represents combination of Activity and Interval.
    Doesn't maintain any of the instances it creates"""

    @abstractmethod
    def get_activity(self, *args, **kwargs) -> Activity:
        """Returns activity belonging to this factory"""

    @abstractmethod
    def get_interval_factory(self) -> IntervalFactory:
        """Returns interval belonging to this factory"""


# todo rename to cycling activity factory
class BikeActivityFactory(ActivityFactory):
    """Factory that represents combination of Cycling Activity and Cycling Interval.
       Doesn't maintain any of the instances it creates
       """

    def get_activity(self, **kwargs) -> Activity:
        """
        Constructs CyclingActivity together with CyclingInterval
        :param id: int - activity id
        :param name: str - activity name
        :param athlete_id: int - athlete id
        :param dataframe: pd.DataFrame - dataframe
        :param [optional] intervals: list[Interval] = field(default_factory=list[Interval])
        :param [optional] type: str = 'bike'
        """

        return CyclingActivity(interval_factory=self.get_interval_factory(), **kwargs)

    def get_interval_factory(self, *args, **kwargs) -> IntervalFactory:
        return CyclingIntervalFactory()

# todo remove testing code
# import pandas as pd
# df = pd.read_csv('../IO/ride.csv')
# f = BikeActivityFactory()
# a = f.get_activity(id=1, name='activity1', dataframe=df)
