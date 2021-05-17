#  Copyright (c) 2021. Sergei Sazonov. Some Rights Reserved

import pandas as pd


class DataWrapper:
    def __init__(self):
        pass

    def get_activity(self, activity_id: str, method: str = 'csv') -> pd.DataFrame:
        if method == 'csv':
            return pd.read_csv(activity_id)
