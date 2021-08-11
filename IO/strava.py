#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import json

import pandas

import IO.strava_io as strava_io
import IO.dbutil as dw
from middleware.activity_new import Activity
from middleware import ActivityFactory, BikeActivityFactory
from flask_login import current_user
import pandas as pd
from cycperf.models import User
from cycperf.models import DBActivity
from cycperf import db


def get_users_last_activity(user_id) -> Activity:
    token = get_token_by_user_id(user_id)
    last_activity = strava_io.retrieve_athlete_last_activity(token)
    streams = strava_io.retrieve_activity_streams(last_activity[0]['id'], token)
    df = pd.DataFrame()
    for stream in streams:
        df[stream['type']] = stream['data']
    factory = BikeActivityFactory()
    activity = factory.get_activity(id=last_activity[0]['id'],
                                    name=last_activity[0]['name'],
                                    athlete_id=last_activity[0]['athlete']['id'],
                                    dataframe=df)
    return activity


def retrieve_and_store_users_activities(user_id) -> None:
    token = get_token_by_user_id(user_id)
    activities = strava_io.retrieve_athlete_activities(token)
    for activity in activities:
        streams = strava_io.retrieve_activity_streams(activity['id'], token)
        laps = strava_io.retrieve_laps_by_activity_id(activity['id'], token)
        df = pd.DataFrame()
        for stream in streams:
            df[stream['type']] = stream['data']
        db_activity = DBActivity(activity_id=activity['id'],
                                 user_id=user_id,
                                 athlete_id=get_strava_id_by_user_id(user_id),
                                 json=activity,
                                 laps=laps,
                                 streams=streams,
                                 df_json=df.to_json(),
                                 )
        db.session.add(db_activity)
        db.session.commit()


def get_token_by_user_id(user_id) -> str:
    user = User.query.filter_by(id=user_id).first()
    return user.strava_access_token


def get_strava_id_by_user_id(user_id) -> str:
    user = User.query.filter_by(id=user_id).first()
    return user.strava_id


def get_activity_by_id(activity_id):
    # todo: add: perform check that activity belongs to user otherwise return None
    token = get_token_by_user_id(current_user.id)
    db_activity = strava_io.retrieve_activity_by_id(activity_id, token)
    streams = strava_io.retrieve_activity_streams(activity_id, token)
    df = pd.DataFrame()
    for stream in streams:
        df[stream['type']] = stream['data']
    activity = Activity(db_activity['id'], db_activity['name'],
                        df=df)
    return activity
