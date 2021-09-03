#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pytest
import pandas as pd
from logic import Bests

@pytest.fixture
def df():
    def _read_dataframe_from_csv(filename: str = "ride.csv", data_path: str = None) -> pd.DataFrame:
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
    return _read_dataframe_from_csv()


@pytest.fixture
def mock_df() -> pd.DataFrame:
    data = [1, 3, 1, 1, 4, 1, 1, 2, 1, 1, 5, 1, 1, 1, 1]
    df = pd.DataFrame(data, columns=['data'])
    return df

class TestMetric:
    pass


class TestLinearMetric:
    pass


class TestBests():

    def test_bests_getter(self):
        assert False

    def test_bests_setter(self):
        assert False

    def test_calculate(self, mock_df):
        best = Bests()
        best.calculate(mock_df)
        assert round(best.bests[5].value - 2, 5) == 0
        assert best.bests[5].windows == [(0, 4), (1, 5), (6, 10), (7, 11)]



class TestPower:
    pass
