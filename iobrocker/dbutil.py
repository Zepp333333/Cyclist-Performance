#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
"""
Database utilities module for HARDIO application
Provides lower level interface to data manipulation in database (and file system for test purposes)
"""
import pathlib
import datetime
from typing import Optional

import pandas as pd
import sqlalchemy.exc

from hardio import db
from hardio.models import Users, DBActivity, UserConfig


class DuplicateActivity(Exception):
    """Custom error in case of attempt to store duplicate activity """

    # todo consider moving to exceptions package
    def __init__(self, id: int, message: str) -> None:
        self.id = id
        self.message = message
        super().__init__(message)


class UserDoesNotExist(Exception):
    """Custom error in case of attempt to store duplicate activity """

    # todo consider moving to exceptions package
    def __init__(self, id: int, message: str) -> None:
        self.id = id
        self.message = message
        super().__init__(message)


def get_user(user_id: int) -> Users:
    """
    Locates in DB and returns user based on user_id
    :return: instance of Users
    """
    user = Users.query.filter_by(id=user_id).first()
    return user if user else None


def get_strava_athlete_id_and_token(user_id: int) -> Optional[tuple[int, str]]:
    """
    Looks up strava athlete_id and strava token for hardio user in database
    :param user_id: hardio user id
    :return: tuple[athlete_id, token]
    """
    try:
        athlete = Users.query.filter_by(id=user_id).first()
        return athlete.strava_id, athlete.strava_access_token  # todo include check and if needed refresh of token
    except AttributeError:
        return None


def get_athlete_info(user_id: int) -> Optional[str]:
    """
        Looks up athlete info in database
        :param user_id: hardio user id
        :return: strava athlete info (JSON string)
        """
    try:
        athlete = Users.query.filter_by(id=user_id).first()
        return athlete.strava_athlete_info
    except AttributeError:
        return None


def update_user(user_id: int, update: dict = None) -> None:
    """
    updates hardio user record in database
    :param user_id: hardio user id
    :param update: dict of filed:value to update
    :return:
    """
    if update is not None:
        user = Users.query.filter_by(id=user_id).first()
        if user:
            for k, v in update.items():
                setattr(user, k, v)
            db.session.commit()
        else:
            raise UserDoesNotExist(id=user_id, message=f"User id {user_id} doesn't exist in database")


def get_activity_from_db(user_id, activity_id: int) -> Optional[DBActivity]:
    """
        Looks up hardio activity pickled object in database
        :param user_id: hardio user id
        :param activity_id: strava activity id
        :return: hardio DBActivity object
        """
    try:
        db_activity = DBActivity.query.filter_by(user_id=user_id, activity_id=activity_id).first()
        return db_activity
    except Exception as e:
        # todo implement SQLAlchemy error handling
        return None


def _store_new_activity(user_id: int,
                        athlete_id: int,
                        activity_id: int,
                        date: datetime.datetime,
                        details: str,
                        name: str,
                        dataframe: str,
                        laps: str,
                        intervals: list[str]) -> None:
    """
    Creates new hardio DBActivity object and stores it in database
    param user_id: hardio user id
    :param athlete_id: strava athlete id
    :param activity_id: strava activity id
    :param date: activity start_date
    :param intervals: list of intervals
    :param laps: list of laps
    :param dataframe: dumped dataframe
    :param details: activity details
    :param name: activity name
    :return: None
    """
    # todo add try/except + handling in IO class. Modify tests accordingly
    db_activity = DBActivity(
        activity_id=activity_id,
        user_id=user_id,
        athlete_id=athlete_id,
        date=date,
        details=details,
        name=name,
        laps=laps,
        dataframe=dataframe,
        intervals=intervals,
    )
    try:
        db.session.add(db_activity)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        raise DuplicateActivity(id=activity_id, message=f"Attempt to store duplicate activity id {activity_id}")


def store_activity(user_id: int,
                   athlete_id: int,
                   activity_id: int,
                   date: datetime.datetime,
                   details: str,
                   name: str,
                   dataframe: str,
                   laps: str,
                   intervals: list[str]) -> None:
    """
    Stores hardio Activity in database
    :param user_id: hardio user id
    :param athlete_id: strava athlete id
    :param activity_id: strava activity id
    :param date: activity start_date
    :param name: activity name
    :param intervals: list of intervals
    :param laps: list of laps
    :param dataframe: dumped dataframe
    :param details: activity details
    :return: None
    """
    # todo rename
    db_activity = DBActivity.query.filter_by(user_id=user_id, activity_id=activity_id).first()
    if db_activity:
        db_activity.intervals = intervals
        db_activity.dataframe = dataframe
        db_activity.name = name
        db.session.commit()
    else:
        _store_new_activity(user_id=user_id,
                            athlete_id=athlete_id,
                            activity_id=activity_id,
                            date=date,
                            intervals=intervals,
                            laps=laps,
                            dataframe=dataframe,
                            details=details,
                            name=name)


def delete_activity(user_id: int, activity_id: int) -> None:
    """
    Deletes stored Activity
    :param user_id: hardio user id
    :param activity_id: strava activity id
    :return: None
    """
    # todo implement: check if activity belongs to user_id
    db_activity = DBActivity.query.filter_by(user_id=user_id, activity_id=activity_id).first()
    db.session.delete(db_activity)
    db.session.commit()


def get_user_id_by_activity_id(activity_id: int) -> Optional[int]:
    """
    Returns user_id associated to an activity in db
    :param activity_id: strava activity id
    :return: user_id or None
    """
    db_activity = DBActivity.query.filter_by(activity_id=activity_id).first()
    if db_activity:
        return db_activity.user_id
    else:
        return None


def read_dataframe_from_csv(filename: str = "ride.csv", data_path: str = None) -> pd.DataFrame:
    """
    Reads csv file containing activity streams and returns pd.DataFrame
    :param data_path: relative path to directory containing csv file
    :param filename: csv file name
    :return: DataFrame with activity streams
    """
    # get relative data folder
    path = pathlib.Path(__file__).parent.parent
    if not data_path:
        data_path = path.joinpath("tests/testing_data").resolve()
    return pd.read_csv(data_path.joinpath(filename))


def get_list_of_activities_in_range(user_id, start_date, end_date) -> list[DBActivity]:
    """
    Queries db to get list if activity ids within date range
    :param user_id: id of the hardio user
    :param start_date: datetime
    :param end_date: datetime
    :return: list of activity id's within given date range
    """
    query = db.session.query(DBActivity).filter(DBActivity.user_id == user_id, DBActivity.date.between(start_date, end_date)).all()
    return query


def save_db_activity(_: DBActivity) -> None:
    db.session.commit()


def read_user_config(user_id: int) -> Optional[str]:
    user_config = UserConfig.query.filter_by(user_id=user_id).first()
    if user_config:
        return user_config.config
    else:
        return None


def save_user_config(user_id: int, config: str) -> None:
    db_config = UserConfig.query.filter_by(user_id=user_id).first()
    if db_config:
        db_config.config = config
    else:
        db_config = UserConfig(user_id=user_id, config=config)
        db.session.add(db_config)
    db.session.commit()
