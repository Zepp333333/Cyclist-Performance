#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import time

from swagger import swagger_client
from swagger.swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()
swagger_client.Configuration.debug = False
configuration.access_token = 'af9670711e08c62d375ec9b7713ad6ed3722b345'

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

