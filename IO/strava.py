#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

# import IO.swagger_client
# import IO.swagger_client.rest
import requests
from config import Config
from IO.strava_auth import BearerAuth
from flask_login import current_user
from cycperf import db
from datetime import datetime


def prep_app_auth_url():
    params = {
        "client_id": Config.STRAVA_APP_CLIENT_ID,
        "redirect_uri": Config.STRAVA_APP_REDIRECT_URI,
        "response_type": "code",
        "scope": "read,profile:read_all,activity:read_all",
        "approval_prompt": "force"
    }
    base_url = Config.STRAVA_AUTH_URL
    return requests.Request('GET', base_url, params=params).prepare().url


def check_auth_code(args):
    return 'code' in args and len(args['code']) == 40


def check_auth_scopes(args):
    if 'scope' not in args:
        return False
    scope = args['scope'].split(',')
    return sorted(scope) == sorted(Config.STRAVA_REQUIRED_SCOPES)


def check_auth_return(args):
    return check_auth_code(args) and check_auth_scopes(args)


def get_known_athlete(token):
    base_url = 'https://www.strava.com/api/v3/athlete'  #todo = move to config
    response = requests.get(base_url, auth=BearerAuth(token))   # todo - add try/except
    return response.json()


def exchange_auth_code_for_token(auth_code):
    params = {
        "client_id": Config.STRAVA_APP_CLIENT_ID,
        "client_secret": Config.STRAVA_APP_CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code"
    }
    base_url = Config.STRAVA_TOKEN_EXCHANGE_URL
    response = requests.post(base_url, params=params)
    return response.json()


def get_first_time_coming_athlete(auth_code):
    token = exchange_auth_code_for_token(auth_code)

    current_user.strava_access_token = token['access_token']
    current_user.strava_token_expires_at = datetime.fromtimestamp(token['expires_at'])
    current_user.strava_refresh_token = token['refresh_token']
    db.session.commit()

    return get_known_athlete(token['access_token'])


def get_athlete(auth_code, token=None):
    if token:
        return get_known_athlete(token)
    return get_first_time_coming_athlete(auth_code)


def get_athlete_last_activity(token):
    params = {
        # "before": "",
        # "after": "",
        "page": 1,
        "per_page": 1
    }
    base_url = "https://www.strava.com/api/v3/athlete/activities"
    response = requests.get(base_url, params=params, auth=BearerAuth(token))
    return response.json()


def get_athlete_activities(token):
    params = {
        # "before": "",
        # "after": "",
        "page": 1,
        "per_page": 10
    }
    base_url = "https://www.strava.com/api/v3/athlete/activities"
    response = requests.get(base_url, params=params, auth=BearerAuth(token))
    return response.json()


def get_activity_by_id(activity_id, token):
    params = {
        'include_all_efforts': ''
    }
    base_url = "https://www.strava.com/api/v3/activities"
    url = f"{base_url}/{activity_id}"
    response = requests.get(url, params=params, auth=BearerAuth(token))
    return response.json()


def get_laps_by_activity_id(activity_id, token):
    params = {
        'include_all_efforts': ''
    }
    base_url = "https://www.strava.com/api/v3/activities"
    url = f"{base_url}/{str(activity_id)}/laps"
    response = requests.get(url, params=params, auth=BearerAuth(token))
    return response.json()


def get_activity_streams(activity_id, token):
    params = {
        'keys': 'time,distance,altitude,latlng,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth',
        'key_by_type': ''
    }
    base_url = "https://www.strava.com/api/v3/activities"
    url = f"{base_url}/{str(activity_id)}/streams"
    response = requests.get(url, params=params, auth=BearerAuth(token))
    return response.json()
