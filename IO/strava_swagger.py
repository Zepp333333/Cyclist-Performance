#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved


import swagger_client
from swagger_client.rest import ApiException
from flask_login import current_user
from flask import redirect, url_for
import IO.dbutil as dbutil
from cycperf.users import routes
import json
from middleware import Activity

from datetime import datetime


def swagger_get_athlete(token: str) -> swagger_client.models.detailed_athlete:
    configuration = swagger_client.Configuration()
    configuration.access_token = token
    api_instance = swagger_client.AthletesApi(swagger_client.ApiClient(configuration))
    try:
        # Get Authenticated Athlete
        api_response = api_instance.get_logged_in_athlete()
        return api_response
    except ApiException as e:
        print("Exception when calling AthletesApi->getLoggedInAthlete: %s\n" % e) # todo - handle the exception


def swagger_get_activity(token: str, activity_id: int) -> swagger_client.models.detailed_activity:
    configuration = swagger_client.Configuration()
    configuration.access_token = token
    api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
    try:
        # Get Authenticated Athlete
        api_response = api_instance.get_activity_by_id(activity_id)
        return api_response
    except ApiException as e:
        print("Exception when calling AthletesApi->getLoggedInAthlete: %s\n" % e)  # todo - handle the exception


def swagger_get_activities(token: str,
                           before: int = datetime.now().timestamp(),
                           after: int = 0,
                           page: int = 1,
                           per_page: int = 30) -> list[swagger_client.models.summary_activity.SummaryActivity]:
    configuration = swagger_client.Configuration()
    configuration.access_token = token
    api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
    try:
        # List Athlete Activities
        api_response = api_instance.get_logged_in_athlete_activities(
            before=before,
            after=after,
            page=page,
            per_page=per_page
        )
        return api_response
    except ApiException as e:
        print("Exception when calling ActivitiesApi->getLoggedInAthleteActivities: %s\n" % e)


def get_athlete(user_id: int = None) -> str:
    if not user_id:
        user_id = current_user.id
    athlete_id, token = dbutil.get_strava_athlete_id_and_token(user_id)
    if not athlete_id:
        return ''
    # Attempt to load athlete from db
    athlete_info = dbutil.get_athlete_info(athlete_id)
    # if not in db -> get from strava API and store in db
    if not athlete_info:
        athlete_info = swagger_get_athlete(token).to_dict()
        dbutil.update_user(user_id=user_id, update={'strava_athlete_info': json.dumps(athlete_info, default=str)})
    return json.dumps(athlete_info, default=str)

def get_activities() -> list:
    user_id = current_user.id
    _, token = dbutil.get_strava_athlete_id_and_token(user_id)
    return swagger_get_activities(token=token)


def get_activity_by_id(activity_id) -> Activity:
    user_id = 1  # current_user.id
    athlete_id, token = dbutil.get_strava_athlete_id_and_token(user_id)
    if not athlete_id:
        return None
    # Attempt to load athlete from db
    strava_activity = dbutil.get_activity(activity_id)
    # if not in db -> get from strava API and store in db
    if not strava_activity:
        strava_activity = swagger_get_activity(token, activity_id)
        # dbutil.store_activity(activitystrava_activity=strava_activity)
    return strava_activity












'''# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()
swagger_client.Configuration.debug = False
configuration.access_token = 'ebf0136139e9554f1aeeb8335776bf4601b17d2a'

# create an instance of the API class
api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
id = 5573827709  # int | The identifier of the activity.
include_all_efforts = True  # bool | To include all segments efforts. (optional)

# try:
#     # Get Activity
#     activity = api_instance.get_activity_by_id(id, include_all_efforts=include_all_efforts)
#     # pprint(api_response)
# except ApiException as e:
#     print("Exception when calling ActivitiesApi->get_activity_by_id: %s\n" % e)

#
# create an instance of the API class
api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
before = 1626090885  # int | An epoch timestamp to use for filtering activities that have taken place before a certain time. (optional)
after = 56  # int | An epoch timestamp to use for filtering activities that have taken place after a certain time. (optional)
page = 56  # int | Page number. Defaults to 1. (optional)
per_page = 30  # int | Number of items per page. Defaults to 30. (optional) (default to 30)

try:
    # List Athlete Activities
    all_activities = api_instance.get_logged_in_athlete_activities()
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_logged_in_athlete_activities: %s\n" % e)


api_instance = swagger_client.AthletesApi(swagger_client.ApiClient(configuration))
try:
    # Get Authenticated Athlete
    user = api_instance.get_logged_in_athlete()

except ApiException as e:
    print("Exception when calling AthletesApi->getLoggedInAthlete: %s\n" % e) # todo - handle the exception

'''


