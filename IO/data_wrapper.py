#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pathlib

import flask_login
import pandas as pd
from cycperf import db
from cycperf.models import DBActivity


class DataWrapper:
    # get relative data folder
    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("IO").resolve()

    def __init__(self):
        pass

    def get_activity(self, activity_id: str, method: str = 'csv') -> pd.DataFrame:
        if method == 'csv':
            return pd.read_csv(self.DATA_PATH.joinpath(activity_id))

    def save_activity(self, activity):
        try:
            db_activity = DBActivity.query.filter_by(activity_id=activity.activity_id).first()
        except:
            db_activity = None

        if db_activity:
            db_activity.intervals = activity.intervals
        else:
            self.create_new_activity(activity)

    def create_new_activity(self, activity):
        pass
