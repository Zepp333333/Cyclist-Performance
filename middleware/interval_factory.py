from abc import ABC, abstractmethod
from .interval import Interval, CyclingInterval


class IntervalFactory(ABC):
    """Factory that represents combination of Activity an Interval.
    Doesn't maintain any of the instances it creates"""

    @abstractmethod
    def get_interval(self) -> Interval:
        """Returns interval belonging to this factory"""


class CyclingIntervalFactory(IntervalFactory):
    def get_interval(self, *args, **kwargs):
        return CyclingInterval()
