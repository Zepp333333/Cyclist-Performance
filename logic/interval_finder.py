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
        filtered_candidates = self._filter_candidates_by_power(candidates, params['power'],
                                                               params['tolerance'])  # filter candidates by power, if provided
        local_max_candidates = self._remove_non_local_max_candidates(filtered_candidates)
        non_overlapping_candidates = self._remove_overlapping_candidates(local_max_candidates, params['duration'])
        return self._make_intervals_list(params['duration'], non_overlapping_candidates.nlargest(params['count']))

    def _produce_candidates(self, dataframe: pd.DataFrame, duration: int):
        candidates = dataframe.rolling(window=duration).mean()  # find all windows of required size
        return candidates

    def _filter_candidates_by_power(self, candidates: pd.DataFrame, power: int, tolerance: float) -> pd.DataFrame:
        if power:  # find all candidate-windows that fall in required power range
            candidates = candidates[self._make_mask(candidates, power, tolerance)]
        return candidates

    def _make_mask(self, means: pd.DataFrame, power: int, tolerance: float) -> pd.DataFrame:
        low_power = power - (power * tolerance)
        high_power = power + (power * tolerance)
        # create boolean mask to select means falling within required power range
        mask = means.between(low_power, high_power, inclusive='both')
        return mask

    def _remove_non_local_max_candidates(self, candidates: pd.DataFrame) -> pd.DataFrame:
        # find local maximums within candidates
        local_max_candidates = candidates[(candidates.shift(1) < candidates) & (candidates.shift(-1) < candidates)]
        return local_max_candidates

    def _remove_overlapping_candidates(self, candidates: pd.DataFrame, duration: int) -> pd.DataFrame:

        def _pick_interval_with_max_mean(_intervals):
            return _intervals.loc[_intervals['mean'] == _intervals['mean'].max()].iloc[0]

        def _make_tuple(_interval) -> tuple[int, int]:
            return int(_interval['start']), int(_interval['end'])

        df = candidates.reset_index()
        df.rename(columns={'index': 'end', 'watts30': 'mean'}, inplace=True)
        df['start'] = df['end'] - duration

        intervals = pd.arrays.IntervalArray.from_arrays(df.start, df.end, closed='both')
        result = []

        for i in intervals:
            overlap_mask = intervals.overlaps(i)
            if overlap_mask.sum() < 1:  # intervals has no overlaps. Append it's left & right  to the result
                result.append((int(i.left), int(i.right)))
            # Otherwise, we interval has overlaps
            overlapping_intervals = df[overlap_mask]  # get overlapping intervals including their means
            selected_interval = _pick_interval_with_max_mean(overlapping_intervals)
            interval_right = int(selected_interval['end'])
            if interval_right not in result:
                result.append(interval_right)
        return candidates.loc[candidates.index.isin(result)]


        # intervals_df = pd.DataFrame(([f - duration, f] for f in candidates.index), columns=['start', 'end'])
        #
        # intervals = pd.arrays.IntervalArray.from_arrays(intervals_df.start, intervals_df.end, closed='both')
        # non_overlapping_candidates = []
        # for i in intervals:
        #     overlap = intervals.overlaps(i)
        #     if overlap.sum() > 1:
        #         indexes = intervals[overlap].right
        #         overlapping_intervals = candidates[indexes]
        #         selected_interval = overlapping_intervals.loc[overlapping_intervals.values == overlapping_intervals.max()]
        #         if selected_interval.index[0] not in non_overlapping_candidates:
        #             non_overlapping_candidates.append(selected_interval.index[0])
        #
        # return non_overlapping_candidates

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
            params['tolerance'] = tolerance / 100
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
    duration = 70
    count = 12
    power = 300
    tolerance = 0.05

    df = read_dataframe_from_csv(filename='12_alps.csv')
    finder = IntervalFinder()
    found = finder.find_manual(duration, count, tolerance, df.watts)
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


# idf = pd.DataFrame(([s, f] for s, f in found), columns=['start', 'end'])
# intervals = pd.arrays.IntervalArray.from_tuples(found)
# for i in intervals:
#     overlap = intervals.overlaps(i)
#     if overlap.sum() > 1:
#         print(intervals.overlaps(i))
#         print(idf[overlap])
