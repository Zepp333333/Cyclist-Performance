#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pytest
import pandas as pd
from logic import Bests
from logic.bests import Best


@pytest.fixture
def df():
    def _read_dataframe_from_csv(filename: str = "zavidovo.csv", data_path: str = None) -> pd.DataFrame:
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
            data_path = path.joinpath("testing_data").resolve()
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


class TestBests:

    def test_bests_getter(self):
        bests = Bests()
        assert bests.bests == {
            1: Best(0, []),
            5: Best(0, []),
            15: Best(0, []),
            60: Best(0, []),
            300: Best(0, []),
            1200: Best(0, []),
            3600: Best(0, [])
        }

    def test_bests_setter(self):
        bests = Bests()
        bests.bests = {
            2: Best(0, []),
            6: Best(0, []),
            16: Best(0, []),
            61: Best(0, []),
            301: Best(0, []),
            1201: Best(0, []),
            3601: Best(0, [])
        }
        assert bests.bests == {
            2: Best(0, []),
            6: Best(0, []),
            16: Best(0, []),
            61: Best(0, []),
            301: Best(0, []),
            1201: Best(0, []),
            3601: Best(0, [])
        }

    def test_calculate(self, mock_df, df):
        bests = Bests()
        bests.calculate(mock_df)
        assert round(float(bests.bests[5].value) - 2, 5) == 0
        assert bests.bests[5].windows == [(0, 4), (1, 5), (6, 10), (7, 11)]

        assert round(float(bests.bests[1].value) - 5, 5) == 0
        assert bests.bests[1].windows == [(10, 10)]

        bests = Bests()
        bests.calculate(df.watts)

        assert round(float(bests.bests[1].value) - 792, 0) == 0
        assert round(float(bests.bests[5].value) - 684.6, 0) == 0
        assert round(float(bests.bests[1200].value) - 288, 0) == 0
        assert round(float(bests.bests[3600].value) - 268, 0) == 0

        assert bests.bests[5].windows == [(27, 31)]
        assert bests.bests[15].windows == [(24, 38)]
        assert bests.bests[1200].windows == [(12, 1211)]
        assert bests.bests[3600].windows == [(12, 3611)]
