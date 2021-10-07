#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class MetricCalculator(ABC):
    """ Strategy interface declares method of Metric calculation"""

    @abstractmethod
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        pass


class Normalized(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'watts' not in df:
            raise KeyError(f"watts stream not found in provided dataframe during call to {self.__class__.__name__} ")
        norm_power = np.sqrt(np.sqrt(np.mean(df['watts'].rolling(30).mean() ** 4)))
        return norm_power


class Intensity(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if not config:
            raise ValueError(f"Attempt to call {self.__class__.__name__} with no config provided")
        if 'ftp' not in config:
            raise KeyError(f"ftp not in config while calling {self.__class__.__name__} ")
        ftp = config['ftp']
        norm_power = Normalized().__call__(df, config)
        intensity = norm_power / ftp
        return intensity


class Load(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if not config:
            raise ValueError(f"Attempt to call {self.__class__.__name__} with no config provided")
        if 'ftp' not in config:
            raise KeyError(f"ftp not in config while calling {self.__class__.__name__} ")
        if 'time' not in df:
            raise KeyError(f"time not in dataframe while calling {self.__class__.__name__} ")
        ftp = config['ftp']
        norm_power = Normalized().__call__(df, config)
        intensity = norm_power / ftp
        moving_time = df['time'].max()
        tss = (moving_time * norm_power * intensity) / (ftp * 3600.0) * 100.0
        return tss


class AveragePower(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'watts' not in df:
            raise KeyError(f"watts stream not found in provided dataframe during call to {self.__class__.__name__} ")
        average_power = df['watts'].mean()
        return average_power


class Work(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'watts' not in df:
            raise KeyError(f"watts stream not found in provided dataframe during call to {self.__class__.__name__} ")
        work = df['watts'].sum(skipna=True) / 1000
        return work


class AverageHR(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'heartrate' not in df:
            raise KeyError(f"heartrate stream not found in provided dataframe during call to {self.__class__.__name__} ")
        average_hr = df['heartrate'].mean()
        return average_hr


class MaxHR(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'heartrate' not in df:
            raise KeyError(f"heartrate stream not found in provided dataframe during call to {self.__class__.__name__} ")
        max_hr = df['heartrate'].max()
        return max_hr


class AverageCadence(MetricCalculator):
    def __call__(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'cadence' not in df:
            raise KeyError(f"heartrate stream not found in provided dataframe during call to {self.__class__.__name__} ")
        average_cadence = df['cadence'].mean()
        return average_cadence


CALCULATORS = {
        'load': Load,
        'intensity': Intensity,
        'average_power': AveragePower,
        'normalized': Normalized,
        'average_hr': AverageHR,
        'max_hr': MaxHR,
        'average_cad': AverageCadence,
        'work': Work,
    }

MEASURES = {
        'load': '',
        'intensity': '',
        'average_power': 'wt',
        'normalized': 'wt',
        'average_hr': 'bpm',
        'max_hr': 'bpm',
        'average_cad': 'rpm',
        'work': 'KJ'
    }
