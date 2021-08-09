#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd

from middleware.activity_test import Activity
from flask_login import current_user
import json
from datetime import datetime


class IO:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.token = None
        self.athlete_id = None

    @property
    def user_id(self) -> int:
        return self.user_id

    def get_athlete_info(self) -> json:
        pass

    def get_list_of_activities(self, start_date: datetime, end_date: datetime):
        pass

    def get_activity_by_id(self, activity_id: int) -> Activity:
        # get activity from DB
        # if not in db -> get from Strava
        # else raise exception
        return Activity()


def get_dataframe(activity_id: int) -> pd.DataFrame:
    """todo Implement"""
    return pd.DataFrame()





