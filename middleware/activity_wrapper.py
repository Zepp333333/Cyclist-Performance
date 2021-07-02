#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import IO.strava as strava
import IO.data_wrapper as dw
from middleware import Activity
from flask_login import current_user
import pandas as pd


def get_users_last_activity(user_id) -> Activity:
    token = current_user.strava_access_token
    last_activity = strava.get_athlete_last_activity(token)
    streams = strava.get_activity_streams(last_activity[0]['id'], token)
    df = pd.DataFrame()
    for stream in streams:
        df[stream['type']] = stream['data']

    activity = Activity(last_activity[0]['name'], df=df)

    return activity
