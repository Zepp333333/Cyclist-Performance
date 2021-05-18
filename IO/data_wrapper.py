#  Copyright (c) 2021. Sergei Sazonov. Some Rights Reserved
import pathlib
import pandas as pd


class DataWrapper:
    # get relative data folder
    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("Data").resolve()

    def __init__(self):
        pass

    def get_activity(self, activity_id: str, method: str = 'csv') -> pd.DataFrame:
        if method == 'csv':
            return pd.read_csv(self.DATA_PATH.joinpath(activity_id))
