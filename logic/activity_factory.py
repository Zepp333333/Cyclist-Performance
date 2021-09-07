#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
from abc import ABC, abstractmethod
from .activity import Activity, CyclingActivity, RunningActivity
from .interval_factory import IntervalFactory, CyclingIntervalFactory, RunningIntervalFactory
from .interval_finder import IntervalFinder


class ActivityFactory(ABC):
    """Factory that represents combination of Activity and Interval.
    Doesn't maintain any of the instances it creates"""

    @abstractmethod
    def get_activity(self, *args, **kwargs) -> Activity:
        """Returns activity belonging to this factory"""

    @abstractmethod
    def get_interval_factory(self) -> IntervalFactory:
        """Returns interval belonging to this factory"""

    @abstractmethod
    def get_interval_finder(self) -> IntervalFinder:
        """Returns interval belonging to this factory"""


class CyclingActivityFactory(ActivityFactory):
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
        :param details: str - dump of the activity details json
        :param [optional] intervals: list[Interval] = field(default_factory=list[Interval])
        :param [optional] type: str = 'bike'

        """

        return CyclingActivity(interval_factory=self.get_interval_factory(),
                               interval_finder=self.get_interval_finder(),
                               **kwargs)

    def get_interval_factory(self, *args, **kwargs) -> IntervalFactory:
        return CyclingIntervalFactory()

    def get_interval_finder(self) -> IntervalFinder:
        """Returns interval belonging to this factory"""
        return IntervalFinder()


class RunningActivityFactory(ActivityFactory):
    """Factory that represents combination of Running Activity and Cycling Interval.
       Doesn't maintain any of the instances it creates
       """

    def get_activity(self, **kwargs) -> Activity:
        """
        Constructs CyclingActivity together with CyclingInterval

        :param id: int - activity id
        :param name: str - activity name
        :param athlete_id: int - athlete id
        :param dataframe: pd.DataFrame - dataframe
        :param details: str - dump of the activity details json
        :param [optional] intervals: list[Interval] = field(default_factory=list[Interval])
        :param [optional] type: str = 'bike'

        """

        return RunningActivity(interval_factory=self.get_interval_factory(),
                               interval_finder=self.get_interval_finder(),
                               **kwargs)

    def get_interval_factory(self, *args, **kwargs) -> IntervalFactory:
        return RunningIntervalFactory()

    def get_interval_finder(self) -> IntervalFinder:
        """Returns interval belonging to this factory"""
        return IntervalFinder()

# todo remove testing code
# import pandas as pd
# df = pd.read_csv('../iobrocker/ride.csv')
# f = CyclingActivityFactory()
# a = f.get_activity(id=1, name='activity1', dataframe=df)
