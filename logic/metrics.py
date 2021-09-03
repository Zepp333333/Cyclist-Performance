#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd


class Metric(ABC):
    METRIC_TYPES = [None, 'custom', 'bests', 'summary']
    DATAFRAME_FIELDS = {
        'Power': 'watts',
        'HR': 'heartrate',
        'Cad': 'cadence',
    }

    def __init__(self, dataframe: pd.DataFrame, metric_type: str = None, graph_type: str = None):
        self.metric_type = metric_type
        self.graph_type = graph_type

        if self.graph_type not in self.METRIC_TYPES:
            raise ValueError('HARDIO Metric object instantiated with a wrong type')

        self.dataframe_field = self.DATAFRAME_FIELDS[self.__class__.__name__]

        self.calculate(dataframe=dataframe)

    @abstractmethod
    def calculate(self, dataframe) -> None:
        """
        Caclulate metrics and populate proerties based on provided dataframe
        :param dataframe: pandas DataFrame
        """


class LinearMetric(Metric, ABC):
    avg: float
    min: float
    max: float

    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)

        if not self.graph_type:
            self.graph_type = 'line'

    @abstractmethod
    def calculate(self, dataframe) -> None:
        """
        Caclulate metrics and populate proerties based on provided dataframe
        :param dataframe: pandas DataFrame
        """

@dataclass
class Best:
    value: float
    windows: list[tuple[int, int]]

class Bests:
    def __init__(self):
        self._bests: dict[int: Best] = {
            1: Best(0, []),
            5: Best(0, []),
            15: Best(0, []),
            60: Best(0, []),
            300: Best(0, []),
            1200: Best(0, []),
            3600: Best(0, [])
        }
        self.graph_type = 'none'

    @property
    def bests(self) -> dict[int: Best]:
        return self._bests

    @bests.setter
    def bests(self, bests: dict[int: Best]) -> None:
        self._bests = bests

    def calculate(self, dataframe: pd.DataFrame) -> None:
        """
        Caclulate metrics and populate proerties based on provided dataframe
        :param dataframe: pandas DataFrame
        """
        for k in self.bests.keys():
            means = dataframe.rolling(window=k).mean()
            max_mean = means.max()
            print(max_mean)
            window_starts = np.where(means.dropna().values == max_mean)[0].tolist()
            windows = [(s, s + (k-1)) for s in window_starts]
            self.bests[k] = Best(max_mean, windows)




class Power(LinearMetric):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)

    def calculate(self, dataframe) -> None:
        """
        Caclulate metrics and populate proerties based on provided dataframe
        :param dataframe: pandas DataFrame
        """
        self.avg = dataframe[self.dataframe_field].mean()
        self.min = dataframe[self.dataframe_field].min()
        self.max = dataframe[self.dataframe_field].max()


def read_dataframe_from_csv(filename: str = "ride.csv", data_path: str = None) -> pd.DataFrame:
    """
    Reads csv file containing activity streams and returns pd.DataFrame
    :param data_path: relative path to directory containing csv file
    :param filename: csv file name
    :return: DataFrame with activity streams
    """
    # get relative data folder
    import pathlib
    path = pathlib.Path(__file__).parent.parent
    if not data_path:
        data_path = path.joinpath("tests/testing_data").resolve()
    return pd.read_csv(data_path.joinpath(filename))

df = read_dataframe_from_csv()
b = Bests()
b.calculate(df.watts)



# @dataclass
# class LinearMetric(Metric):
#     @dataclass
#     class Metric(ABC):
#         METRIC_TYPES = [None, 'custom', 'bests', 'summary']
#         DATAFRAME_FIELDS = {
#             'Power': 'watts',
#             'HR': 'heartrate',
#             'Cad': 'cadence',
#         }
#
#         type: str = None
#         graph_type: str = None
#
#         avg: float = None
#         min: float = None
#         max: float = None
#
#         dataframe_field: str = None
#
#         def __post_init__(self):
#             if self.type not in self.METRIC_TYPES:
#                 raise ValueError('HARDIO Metric object instantiated with a wrong type')
#
#             self.dataframe_field = self.DATAFRAME_FIELDS[self.__class__.__name__]
#
#     @dataclass
#     class LinearMetric(Metric):
