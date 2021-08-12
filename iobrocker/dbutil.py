#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pathlib
from typing import Optional

import pandas as pd

from cycperf import db
from cycperf.models import User, DBActivity


def get_strava_athlete_id_and_token(user_id):
    try:
        athlete = User.query.filter_by(id=user_id).first()
        return athlete.strava_id, athlete.strava_access_token  # todo include check and if needed refresh of token
    except AttributeError:
        return None


def get_athlete_info(athlete_id):
    print("dbutil.get_athlete_info fired")
    try:
        athlete = User.query.filter_by(strava_id=athlete_id).first()
        return athlete.strava_athlete_info
    except AttributeError:
        return None


def update_user(user_id: int, update: dict = None):
    if update is not None:
        user = User.query.filter_by(id=user_id).first()
        for k, v in update.items():
            setattr(user, k, v)
        db.session.commit()


def get_activity_from_db(activity_id: int) -> Optional[bytes]:
    try:
        db_activity = DBActivity.query.filter_by(activity_id=activity_id).first()
        return db_activity.pickle
    except Exception as e:
        # todo implement SQLAlchemy error handling
        return None


def create_new_activity(user_id: int, athlete_id: int, activity_id: int, pickle: bytes):
    # db_activity = DBActivity(activity_id=activity_id,
    #                          user_id=user_id,
    #                          athlete_id=athlete_id,
    #                          pickle=pickle)
    db_activity = DBActivity()
    db_activity.user_id = user_id
    db_activity.athlete_id = athlete_id
    db_activity.activity_id = activity_id
    db_activity.pickle = pickle
    db.session.add(db_activity)
    db.session.commit()


def store_cycperf_activity(user_id: int, athlete_id: int, activity_id: int, pickle: bytes):
    # todo rename
    db_activity = DBActivity.query.filter_by(activity_id=activity_id).first()
    if db_activity:
        db_activity.pickle = pickle
        db.session.commit()
    else:
        create_new_activity(user_id, athlete_id, activity_id, pickle)


def delete_activity(user_id: int, activity_id: int) -> None:
    # todo implement: check if activity belongs to user_id
    db_activity = DBActivity.query.filter_by(activity_id=activity_id).first()
    db.session.delete(db_activity)
    db.session.commit()


def get_user_id_by_activity_id(activity_id: int) -> Optional[int]:
    """Returns user_id associated to an activity in db"""
    db_activity = DBActivity.query.filter_by(activity_id=activity_id).first()
    if db_activity:
        return db_activity.user_id
    else:
        return None


def read_dataframe_from_csv(activity_id):
    # get relative data folder
    path = pathlib.Path(__file__).parent.parent
    data_path = path.joinpath("iobrocker").resolve()
    return pd.read_csv(data_path.joinpath(activity_id))
