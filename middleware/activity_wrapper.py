#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import json

import IO.strava as strava
import IO.data_wrapper as dw
from middleware import Activity
from flask_login import current_user
import pandas as pd
from cycperf.models import User
from cycperf.models import DBActivity
from cycperf import db


def get_users_last_activity(user_id) -> Activity:
    token = get_token_by_user_id(user_id)
    last_activity = strava.retrieve_athlete_last_activity(token)
    streams = strava.retrieve_activity_streams(last_activity[0]['id'], token)
    df = pd.DataFrame()
    for stream in streams:
        df[stream['type']] = stream['data']

    activity = Activity(last_activity[0]['name'], df=df)

    return activity


def retrieve_and_store_users_activities(user_id) -> None:
    token = get_token_by_user_id(user_id)
    activities = strava.retrieve_athlete_activities(token)
    for activity in activities:
        streams = strava.retrieve_activity_streams(activity['id'], token)
        laps = strava.retrieve_laps_by_activity_id(activity['id'], token)
        df = pd.DataFrame()
        for stream in streams:
            df[stream['type']] = stream['data']
        db_activity = DBActivity(activity_id=activity['id'],
                                 user_id=user_id,
                                 athlete_id=get_strava_id_by_user_id(user_id),
                                 json=activity,
                                 laps=laps,
                                 streams=streams,
                                 df=df.to_json(),
                                 )
        db.session.add(db_activity)
        db.session.commit()


def get_token_by_user_id(user_id) -> str:
    user = User.query.filter_by(id=user_id).first()
    return user.strava_access_token


def get_strava_id_by_user_id(user_id) -> str:
    user = User.query.filter_by(id=user_id).first()
    return user.strava_id
