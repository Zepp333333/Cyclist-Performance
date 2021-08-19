#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved


import json
from datetime import datetime
from typing import Optional

import swagger_client
from flask_login import current_user
from swagger_client.rest import ApiException

from iobrocker import dbutil


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
                           per_page: int = 30,
                           async_req=True) -> list[swagger_client.models.summary_activity.SummaryActivity]:
    # todo make possible syncronous requests. No asyc behaviour is hardcoded
    configuration = swagger_client.Configuration()
    configuration.access_token = token
    api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
    try:
        # List Athlete Activities
        thread = api_instance.get_logged_in_athlete_activities(
            async_req=async_req,
            before=before,
            after=after,
            page=page,
            per_page=per_page
        )
        api_response = thread.get()
        return api_response
    except ApiException as e:
        print("Exception when calling ActivitiesApi->getLoggedInAthleteActivities: %s\n" % e)


def swagger_get_activity_streams(token: str, activity_id: int) -> Optional[swagger_client.models.stream_set.StreamSet]:

    configuration = swagger_client.Configuration()
    configuration.access_token = token
    api_instance = swagger_client.StreamsApi(swagger_client.ApiClient(configuration))
    try:
        keys = ['time', 'distance', 'altitude', 'latlng',
                'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp',
                'moving', 'grade_smooth']
        api_response = api_instance.get_activity_streams(id=activity_id, keys=keys, key_by_type=True)
        return api_response
    except ApiException as e:
        print("Exception when calling AthletesApi->getLoggedInAthlete: %s\n" % e)  # todo - handle the exception


def get_athlete(user_id: int = None) -> str:
    if not user_id:
        user_id = current_user.id
    athlete_id, token = dbutil.get_strava_athlete_id_and_token(user_id)
    if not athlete_id:
        return ''
    # Attempt to load athlete from db
    athlete_info = dbutil.get_athlete_info(user_id)
    # if not in db -> get from strava API and store in db
    if not athlete_info:
        athlete_info = swagger_get_athlete(token).to_dict()
        dbutil.update_user(user_id=user_id, update={'strava_athlete_info': json.dumps(athlete_info, default=str)})
    return json.dumps(athlete_info, default=str)


def get_activities(user_id: int = None, **kwargs) -> list:
    user_id = user_id if user_id else current_user.id
    _, token = dbutil.get_strava_athlete_id_and_token(user_id)
    return swagger_get_activities(token=token, **kwargs)


def get_activity_by_id(activity_id: int, user_id: int = None) -> Optional[swagger_client.models.DetailedAthlete]:
    if not user_id:
        user_id = current_user.id
    athlete_id, token = dbutil.get_strava_athlete_id_and_token(user_id)
    if not athlete_id:
        return None
    strava_activity = swagger_get_activity(token, activity_id)
    # dbutil.store_strava_activity(strava_activity=strava_activity, user_id=user_id, athlete_id=athlete_id)
    return strava_activity


def get_activity_streams(activity_id: int, user_id: int = None) -> Optional[swagger_client.models.stream_set.StreamSet]:
    if not user_id:
        user_id = current_user.id
    athlete_id, token = dbutil.get_strava_athlete_id_and_token(user_id)
    if not athlete_id:
        return None
    streams = swagger_get_activity_streams(token=token, activity_id=activity_id)
    return streams


def get_last_activity_id(user_id: int = None) -> Optional[int]:
    activities = get_activities(user_id=user_id, page=1, per_page=1)
    return activities[0].id












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


