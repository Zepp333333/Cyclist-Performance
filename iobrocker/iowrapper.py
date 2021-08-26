#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
"""
Provides High level interface to Strava API and Database requests
"""
# todo rename module

import json
from datetime import datetime
from typing import Optional

import pandas as pd
import swagger_client.models
from flask_login import current_user

from iobrocker import dbutil, strava_auth
from iobrocker.utils import CustomEncoder, CustomDecoder, get_activity_factory
from iobrocker import strava_swagger
from middleware import Activity
from middleware import CyclingActivityFactory


class ActivityNotFoundInDB(Exception):
    """Custom error in case activity not in DB"""

    # todo consider moving to exceptions package
    def __init__(self, id: int, message: str) -> None:
        self.id = id
        self.message = message
        super().__init__(message)


class IO:
    """
    Provides High level interface to Strava API and Database requests
    """

    def __init__(self, user_id: int = None, token_refresh=True):
        self.user_id = user_id if user_id else current_user.id

        if token_refresh and self.is_strava_token_expired():
            self.refresh_token()

    def build_mock_up_ride(self):
        df = dbutil.read_dataframe_from_csv(filename='ride.csv')
        factory = CyclingActivityFactory()
        return factory.get_activity(id=1, athlete_id=0, name='My ride', dataframe=df, date=datetime.now())

    def get_athlete_info(self) -> json:
        raise NotImplemented

    def get_list_of_activities(self, start_date: datetime, end_date: datetime):
        raise NotImplemented

    def get_strava_activities(self, **kwargs) -> list[Activity]:
        result = []
        strava_activities = strava_swagger.get_activities(self.user_id, **kwargs)
        for strava_activity in strava_activities:
            result.append(self.make_cp_activity_from_strava_activity(strava_activity))
        return result

    def get_cp_activity_by_id(self, activity_id: int) -> Activity:
        db_activity = dbutil.get_activity_from_db(activity_id=activity_id)
        if db_activity:
            details = json.loads(db_activity.details, cls=CustomDecoder)
            factory = get_activity_factory(details)
            return factory.get_activity(
                id=db_activity.activity_id,
                athlete_id=db_activity.athlete_id,
                name=details['name'],
                date=db_activity.date,
                dataframe=pd.read_json(db_activity.dataframe),
                details=details,
                intervals=json.loads(db_activity.intervals, cls=CustomDecoder)
            )
        else:
            raise ActivityNotFoundInDB(id=activity_id,
                                       message=f"Activity {activity_id} not found in DB")

    def save_activities(self, activities: list[Activity]) -> None:
        """
        Saves list of Activity objects to database
        :param activities: list of Activity objects
        :return: None
        """
        for activity in activities:
            self.save_activity(activity)

    def save_activity(self, activity: Activity) -> None:
        """Saves Activity object to db"""
        dbutil.store_activity(
            user_id=self.user_id,
            athlete_id=activity.athlete_id,
            activity_id=activity.id,
            date=activity.date,
            details=json.dumps(activity.details, cls=CustomEncoder, indent=4),
            dataframe=activity.dataframe.to_json(indent=4),
            laps='',
            intervals=json.dumps(activity.intervals, cls=CustomEncoder, indent=4)
        )

    def delete_activity_by_id(self, activity_id):
        """wrapper function to delete activity by id"""
        db_activity_id = dbutil.get_user_id_by_activity_id(activity_id)
        if db_activity_id == self.user_id:
            dbutil.delete_activity(user_id=self.user_id, activity_id=activity_id)
        else:
            raise  # todo implement exception

    def get_strava_activity_by_id(self, activity_id: int, get_streams: bool = True) -> Optional[Activity]:

        strava_activity = strava_swagger.get_activity_by_id(activity_id=int(activity_id),
                                                            user_id=self.user_id)
        if strava_activity:
            activity = self.make_cp_activity_from_strava_activity(strava_activity.to_dict(), get_streams)
            return activity
        else:
            return None

    def get_last_activity(self) -> Optional[Activity]:
        last_activity_id = strava_swagger.get_last_activity_id(user_id=self.user_id)
        return self.get_strava_activity_by_id(last_activity_id)

    def is_strava_authorized(self):
        _, token = dbutil.get_strava_athlete_id_and_token(self.user_id)
        return True if token else False

    def is_strava_token_expired(self) -> bool:
        # todo refactor | simplify -> move out somewhere
        expiration = dbutil.get_user(self.user_id).strava_token_expires_at
        if expiration:
            return strava_auth.is_token_expired(expiration)
        return False

    def refresh_token(self):
        strava_auth.refresh_access_token(self.user_id)

    def make_cp_activity_from_strava_activity(self, strava_activity: dict, get_streams: bool = True) -> Activity:
        """
        Builds cycperf activity object based on strava detailed activity
        :param strava_activity:
        :return: Activity object
        :param get_streams: [Optional] Default True. Controls whether to call Strava API to get streams or not. Produce activity with
        empty dataframe in case False.
        """
        if get_streams:
            streams = strava_swagger.get_activity_streams(strava_activity['id'], self.user_id)
            dataframe = _make_df(streams)
        else:
            dataframe = pd.DataFrame()

        factory = get_activity_factory(strava_activity)
        activity = factory.get_activity(
            id=strava_activity['id'],
            date=strava_activity['start_date'],
            athlete_id=strava_activity['athlete']['id'],
            name=strava_activity['name'],
            dataframe=dataframe,
            details=strava_activity
        )
        return activity


def _make_df(streams: swagger_client.models.StreamSet) -> pd.DataFrame:
    """
    Helper function - builds DstaFrame out of strava StreamSet
    :param streams: strava StreamSet
    :return: DataFrame
    """
    df = pd.DataFrame()
    streams_dict = streams.to_dict()
    for key in streams_dict.keys():
        if streams_dict[key]:
            df[key] = streams_dict[key]['data']
    return df
