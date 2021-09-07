#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pandas as pd
from abc import ABC, abstractmethod


class Derivative(ABC):
    pass


class MovingAverage(Derivative):
    def __init__(self, windows: int) -> None:
        super().__init__()
        self.window = windows

    def produce(self, df: pd.DataFrame) -> list[float]:
        moving_average = df.rolling(window=self.window).mean()
        return moving_average







