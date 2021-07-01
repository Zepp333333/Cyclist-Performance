#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

# from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from config import Config


def get_athlete(token):
    # Configure OAuth2 access token for authorization: strava_oauth
    swagger_client.configuration.access_token = token

    # create an instance of the API class
    api_instance = swagger_client.AthletesApi()

    try:
        # Get Authenticated Athlete
        api_response = api_instance.get_logged_in_athlete()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AthletesApi->getLoggedInAthlete: %s\n" % e)
