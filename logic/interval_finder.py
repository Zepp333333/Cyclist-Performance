#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pandas as pd


class IntervalFinder:
    def find_manual(self,
                    duration: int,
                    count: int,
                    tolerance: float,
                    dataframe: pd.DataFrame,
                    power: int = None) -> list[tuple[int, int]]:

        params: {} = self.set_params(duration=duration, count=count, tolerance=tolerance, power=power)
        candidates = self._produce_candidates(dataframe, params['duration'])
        filtered_candidates = self._filter_candidates(candidates, params['power'],
                                                      params['tolerance'])  # filter candidates by power, if provided
        best_candidates = self._select_candidates(filtered_candidates, params['count'])
        return self._make_intervals_list(params['duration'], best_candidates)

    def _produce_candidates(self, dataframe: pd.DataFrame, duration: int):
        candidates = dataframe.rolling(window=duration).mean()  # find all windows of required size
        return candidates

    def _filter_candidates(self, candidates: pd.DataFrame, power: int, tolerance: float) -> pd.DataFrame:
        if power:  # find all candidate-windows that fall in required power range
            candidates = candidates[self._make_mask(candidates, power, tolerance)]
        return candidates

    def _make_mask(self, means: pd.DataFrame, power: int, tolerance: float) -> pd.DataFrame:
        low_power = power - (power * tolerance)
        high_power = power + (power * tolerance)
        # create boolean mask to select means falling within required power range
        mask = means.between(low_power, high_power, inclusive='both')
        return mask

    def _select_candidates(self, candidates: pd.DataFrame, count: int) -> pd.DataFrame:
        # find local maximums within candidates
        local_max_candidates = candidates[(candidates.shift(1) < candidates) & (candidates.shift(-1) < candidates)]
        # select required number of top candidates
        selected_candidates = local_max_candidates.nlargest(count)
        return selected_candidates

    def _make_intervals_list(self, duration: int, selected_candidates: pd.DataFrame) -> list[tuple[int, int]]:
        intervals = []
        for i in selected_candidates.index:
            intervals.append((i - duration, i))
        return intervals

    def set_params(self, duration: int, count: int, tolerance: float, power: int) -> dict:
        params = {}
        if not duration or duration == 0:
            params['duration'] = 300
        else:
            params['duration'] = duration
        if not count or count == 0:
            params['count'] = 5
        else:
            params['count'] = count
        if not tolerance or tolerance == 0:
            params['tolerance'] = 0.2
        else:
            params['tolerance'] /= 100
        if not power or power == 0:
            params['power'] = None
        else:
            params['power'] = power
        return params


# todo: remove test code below
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


def test():
    length = 240
    count = 2
    power = 290
    tolerance = 0.05

    df = read_dataframe_from_csv(filename='20_apr.csv')
    finder = IntervalFinder()
    found = finder.find_manual(length, count, tolerance, df.watts)
    print(found)

    list_intervals = []
    for r in found:
        list_intervals.extend(list(range(r[0], r[1])))

    import numpy as np

    newdf = pd.DataFrame({'watts': df.watts})
    newdf['intervals'] = np.nan
    for i in list_intervals:
        newdf.loc[i, 'intervals'] = power

    import plotly.graph_objects as go

    fig = go.Figure()
    # Full line
    fig.add_scattergl(x=newdf.index, y=newdf.watts, line={'color': 'blue'})
    # Above threshhgold
    fig.add_scattergl(y=newdf.intervals, line={'color': 'red'})

    fig.show()
