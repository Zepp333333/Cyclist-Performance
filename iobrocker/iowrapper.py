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

from hardio.models import DBActivity
from iobrocker import dbutil, strava_auth
from iobrocker import strava_swagger
from logic import Activity
from logic import ActivityFactory, PresentationActivity


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
        self.user_id = user_id

        if token_refresh and self.is_strava_token_expired():
            self.refresh_token()

    def build_mock_up_ride(self):
        df = dbutil.read_dataframe_from_csv(filename='ride.csv')
        factory = ActivityFactory.get_activity_factory({'type': "Ride"})
        return factory.get_activity(id=1, athlete_id=0, name='My ride', dataframe=df, date=datetime.now())

    def get_athlete_info(self) -> json:
        raise NotImplemented

    def get_list_of_activities_in_range(self, start_date: datetime, end_date: datetime) -> list[PresentationActivity]:
        activities = dbutil.get_list_of_activities_in_range(self.user_id, start_date, end_date)
        return [self._make_presentation_activity(a) for a in activities]



    def get_activities_from_strava(self, get_streams: bool = False, **kwargs) -> list[Activity]:
        result = []
        strava_activities = strava_swagger.get_activities(self.user_id, **kwargs)
        for strava_activity in strava_activities:
            result.append(self.make_hardio_activity_from_strava_activity(strava_activity.to_dict(), get_streams))
            self.save_activities(result)
        return result

    def get_hardio_activity_by_id(self, activity_id: int, get_streams: bool = True) -> Activity:
        db_activity = dbutil.get_activity_from_db(user_id=self.user_id, activity_id=activity_id)
        if not db_activity:
            raise ActivityNotFoundInDB(id=activity_id, message=f"Activity {activity_id} not found in DB")
        return self._make_hardio_activity_from_db_activity(db_activity, get_streams)

    def _make_hardio_activity_from_db_activity(self, db_activity: DBActivity, get_streams: bool = True) -> Activity:
        dataframe = pd.read_json(db_activity.dataframe)
        if dataframe.empty and get_streams:
            streams = strava_swagger.get_activity_streams(activity_id=db_activity.activity_id, user_id=self.user_id)
            dataframe = _make_df(streams)
            db_activity.dataframe = dataframe.to_json(indent=4)
            dbutil.save_db_activity(db_activity)

        details = Activity.read_details_from_json(db_activity.details)
        factory = ActivityFactory.get_activity_factory(details)
        return factory.get_activity(
            id=db_activity.activity_id,
            athlete_id=db_activity.athlete_id,
            name=db_activity.name if db_activity.name else details['name'],
            date=db_activity.date,
            dataframe=pd.read_json(db_activity.dataframe),
            details=details,
            intervals=Activity.read_intervals_from_json(db_activity.intervals)
        )

    def save_activities(self, activities: list[Activity]) -> None:
        """
        Saves list of Activity objects to database
        :param activities: list of Activity objects
        :return: None
        """
        for activity in activities:
            try:
                self.save_activity(activity)
            except Exception as e:
                # todo, narrow-down, handle
                pass

    def save_activity(self, activity: Activity) -> None:
        """Saves Activity object to db"""
        dbutil.store_activity(
            user_id=self.user_id,
            athlete_id=activity.athlete_id,
            activity_id=activity.id,
            date=activity.date,
            name=activity.name,
            details=activity.details_to_json(),
            dataframe=activity.dataframe.to_json(indent=4),
            laps='',
            intervals=activity.intervals_to_json()
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
            activity = self.make_hardio_activity_from_strava_activity(strava_activity.to_dict(), get_streams)
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

    def make_hardio_activity_from_strava_activity(self, strava_activity: dict, get_streams: bool = True) -> Activity:
        """
        Builds hardio activity object based on strava detailed activity
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

        factory = ActivityFactory.get_activity_factory(strava_activity)
        activity = factory.get_activity(
            id=strava_activity['id'],
            date=strava_activity['start_date'],
            athlete_id=strava_activity['athlete']['id'],
            name=strava_activity['name'],
            dataframe=dataframe,
            details=strava_activity
        )
        return activity

    def get_activities_by_date(self, ):
        pass

    def _make_presentation_activity(self, a: DBActivity) -> PresentationActivity:
        return PresentationActivity(
            id=a.activity_id,
            date=a.date,
            name=self.get_name_of_activity(a),
            type=self.get_type_of_activity(a)
        )

    def get_type_of_activity(self, a: DBActivity) -> str:
        d = Activity.read_details_from_json(a.details)
        return d['type']

    def get_name_of_activity(self, a: DBActivity) -> str:
        if a.name:
            return a.name
        else:
            d = Activity.read_details_from_json(a.details)
            return d['name']

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
