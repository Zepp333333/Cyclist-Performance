#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import requests
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

AUTH_URL = "https://www.strava.com/oauth/"
ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
ACTIVITY_URL_BASE = "https://www.strava.com/api/v3/activities/"
STREAM_ULR_BASE = "https://www.strava.com/api/v3/activities/"
APP_CLIENT_ID = 50434
APP_CLIENT_SECRET = '1ac85eaaa5fcf4a1b4efa75197a81bc4b00464db'
APP_REDIRECT_URI = "http://localhost"

# Initializeing variables
access_token = None
athlete_auth_code = 'fc37362fd1073891cfe170fdb18f3191f2a3a347'

def get_athlete_authorization_code():
    ### STUB ###
    return athlete_auth_code  ### STUB todo get the function done as soon as we have web app
    ### STUB - pieces of real code -> below
    url = AUTH_URL + "authorize"
    param = {'client_id': APP_CLIENT_ID,
             'redirect_uri': APP_REDIRECT_URI,
             'response_type': 'code',
             'scope': 'activity:read_all'}
    r = requests.get(url, params=param)
    return r.content

layout = html.Div([
    html.Content(get_athlete_authorization_code())
])
# layout = html.Div(get_athlete_authorization_code())
