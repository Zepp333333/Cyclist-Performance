#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class DataFieldStrategy(ABC):
    """ Strategy interface declares method of DataField calculation"""

    @abstractmethod
    def calculate(self, df: pd.DataFrame, config: dict = None) -> float:
        pass


class Normalized(DataFieldStrategy):
    def calculate(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'watts' not in df:
            raise KeyError(f"watts stream not found in provided dataframe during call to {self.__class__.__name__} ")
        norm_power = np.sqrt(np.sqrt(np.mean(df['watts'].rolling(30).mean() ** 4)))
        return norm_power


class Intensity(DataFieldStrategy):
    def calculate(self, df: pd.DataFrame, config: dict = None) -> float:
        if not config:
            raise ValueError(f"Attempt to call {self.__class__.__name__} with no config provided")
        if 'ftp' not in config:
            raise KeyError(f"ftp not in config while calling {self.__class__.__name__} ")
        ftp = config['ftp']
        norm_power = Normalized().calculate(df, config)
        intensity = norm_power / ftp
        return intensity


class Load(DataFieldStrategy):
    def calculate(self, df: pd.DataFrame, config: dict = None) -> float:
        if not config:
            raise ValueError(f"Attempt to call {self.__class__.__name__} with no config provided")
        if 'ftp' not in config:
            raise KeyError(f"ftp not in config while calling {self.__class__.__name__} ")
        if 'time' not in df:
            raise KeyError(f"time not in dataframe while calling {self.__class__.__name__} ")
        ftp = config['ftp']
        norm_power = Normalized().calculate(df, config)
        intensity = norm_power / ftp
        moving_time = df['time'].max()
        tss = (moving_time * norm_power * intensity) / (ftp * 3600.0) * 100.0
        return tss


class AveragePower(DataFieldStrategy):
    def calculate(self, df: pd.DataFrame, config: dict = None) -> float:
        if 'watts' not in df:
            raise KeyError(f"watts stream not found in provided dataframe during call to {self.__class__.__name__} ")
        average_power = df['watts'].mean()
        return average_power
