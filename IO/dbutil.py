#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import json
import pathlib

import flask_login
import pandas as pd

import swagger_client
from cycperf import db
from cycperf.models import User, DBActivity


def get_strava_athlete_id_and_token(user_id):
    try:
        athlete = User.query.filter_by(id=user_id).first()
        return athlete.strava_id, athlete.strava_access_token #todo include check and if needed refresh of tocken
    except AttributeError:
        return None


def get_athlete_info(athlete_id):
    print("dbutil.get_athlete_info fired")
    try:
        athlete = User.query.filter_by(strava_id=athlete_id).first()
        return athlete.strava_athlete_info
    except AttributeError:
        return None


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


def update_user(user_id: int, update: dict = None):
    if update is not None:
        user = User.query.filter_by(id=user_id).first()
        for k, v in update.items():
            setattr(user, k, v)
        db.session.commit()


def get_activity(activity_id):
    return None


def store_activity(strava_activity: swagger_client.DetailedActivity,
                   user_id: int,
                   athlete_id: int,
                   ):
    laps = [lap.to_dict() for lap in strava_activity.laps]
    db_activity = DBActivity(activity_id=strava_activity.id,
                             user_id=user_id,
                             athlete_id=athlete_id,
                             json=json.dumps(strava_activity, default=str),
                             laps=json.dumps(laps, default=str)
                             )
    db.session.add(db_activity)
    db.session.commit()
