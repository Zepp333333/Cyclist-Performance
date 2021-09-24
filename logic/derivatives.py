#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pandas as pd
from abc import ABC, abstractmethod


class Derivative(ABC):
    @abstractmethod
    def produce(self, df: pd.DataFrame, stream_name: str, time_stream_name: str = 'time') -> list[float]:
        """ Produce list containing derivative stream"""


class MovingAverage(Derivative):
    def __init__(self, stream: str, window: int = 30) -> None:
        super().__init__()
        self.stream = stream
        self.window = window

    def produce(self, df: pd.DataFrame, stream_name: str, time_stream_name: str = 'time') -> list[float]:
        moving_average = df[self.stream].rolling(window=self.window).mean()
        return moving_average


class RunningPace(Derivative):
    def produce(self, df: pd.DataFrame, stream_name: str, time_stream_name: str = 'time') -> list[float]:
        pace_series = df[time_stream_name] / df['distance'] * 1000
        return pace_series.to_list()
