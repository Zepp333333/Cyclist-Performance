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


df = read_dataframe_from_csv(filename='zavidovo.csv')
m = MovingAverage(30)

ma = m.produce(df.watts)
newdf = pd.DataFrame({'watts': df.watts, 'ma': ma})

import plotly.graph_objects as go

fig = go.Figure()
# Full line
fig.add_scattergl(x=newdf.index, y=newdf.ma, line={'color': 'blue'})
# Above threshhgold
fig.add_scattergl(y=newdf.ma.where(newdf.ma >= 250), line={'color': 'red'})

fig.show()


