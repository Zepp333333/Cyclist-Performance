#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from dataclasses import dataclass

import pandas as pd


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
            window_starts = means.loc[means.values == float(max_mean)].index.to_list()
            windows = [(s - k + 1, s) for s in window_starts]
            self.bests[k] = Best(float(max_mean), windows)
