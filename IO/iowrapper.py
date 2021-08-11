#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved


import json
from datetime import datetime

import pandas as pd
import swagger_client.models
from flask_login import current_user

from IO import dbutil
from IO import strava_swagger
from middleware import Activity
from middleware import ActivityFactory, BikeActivityFactory


class ActivityNotFoundInDB(Exception):
    """Custom error in case activity not in DB"""

    # todo consider moving to exceptions package
    def __init__(self, id: int, message: str) -> None:
        self.id = id
        self.message = message
        super().__init__(message)


def make_df(streams: swagger_client.models.StreamSet) -> pd.DataFrame:
    df = pd.DataFrame()
    streams_dict = streams.to_dict()
    for key in streams_dict.keys():
        df[key] = streams_dict[key]['data']
    return df


class IO:
    def __init__(self, user_id: int = None):
        self.user_id = user_id if user_id else current_user.id

    def get_athlete_info(self) -> json:
        pass

    def get_list_of_activities(self, start_date: datetime, end_date: datetime):
        pass

    def get_activity_by_id(self, activity_id: int) -> Activity:
        # try getting activity pickle from DB, deserialize and return
        pickle = dbutil.get_activity_from_db(activity_id=activity_id)
        if pickle:
            return Activity.from_pickle(pickle)
        else:
            raise ActivityNotFoundInDB(id=activity_id,
                                       message=f"Activity {activity_id} not found in DB")

    def save_activity(self, activity: Activity):
        """Saves Activity object to db"""
        dbutil.store_cycperf_activity(
            user_id=self.user_id,
            athlete_id=activity.athlete_id,
            activity_id=activity.id,
            pickle=activity.pickle(),
        )

    def delete_activity_by_id(self, activity_id):
        """wrapper function to delete activity by id"""
        db_activity_id = dbutil.get_user_id_by_activity_id(activity_id)
        if db_activity_id == self.user_id:
            dbutil.delete_activity(user_id=self.user_id, activity_id=activity_id)
        else:
            raise  # todo implement exception

    def get_strava_activity_by_id(self, activity_id: int) -> Activity:

        strava_activity = strava_swagger.get_activity_by_id(activity_id=int(activity_id),
                                                            user_id=self.user_id)
        streams = strava_swagger.get_activity_streams(activity_id=int(activity_id),
                                                      user_id=self.user_id)
        df = make_df(streams)
        activity = BikeActivityFactory().get_activity(
            id=activity_id,
            athlete_id=strava_activity.athlete.id,
            name=strava_activity.name,
            dataframe=df
        )
        return activity
