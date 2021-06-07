#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

# import IO.swagger_client
# import IO.swagger_client.rest
import requests

AUTH_URL = "https://www.strava.com/oauth/authorize"
APP_CLIENT_ID = 50434
APP_CLIENT_SECRET = '1ac85eaaa5fcf4a1b4efa75197a81bc4b00464db'
APP_REDIRECT_URI = "http://localhost"


def strava_oauth(client_id, client_secret):
    params = {
        "client_id": APP_CLIENT_ID,
        "redirect_uri": APP_REDIRECT_URI,
        "response_type": "code",
        "scope": "read,profile:read_all,activity:read",
        "approval_prompt": "force"
    }
    r = requests.get(AUTH_URL, params=params)
    return r.content


r = strava_oauth(APP_CLIENT_ID, APP_CLIENT_SECRET)
