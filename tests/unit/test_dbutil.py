#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from datetime import datetime

import pandas
import pytest

from cycperf.models import DBActivity, Users
from iobrocker import dbutil, dbutil_admin
from middleware import Activity, CyclingActivityFactory


@pytest.fixture(scope='module')
def populate_db(test_client):
    # add a user to db
    dbutil_admin.add_user(username="JohnTest",
                          email="johnsnow@gmail.com",
                          password="Pass@word1",
                          strava_id=123456,
                          strava_access_token="token",
                          strava_token_expires_at=datetime(2001, 11, 23),
                          strava_refresh_token="refresh_token",
                          strava_athlete_info="info")

    # # add an activity to db
    # mock_dataframe = dbutil.read_dataframe_from_csv()
    # activity = CyclingActivityFactory().get_activity(id=999999,
    #                                                  name="Bike Ride",
    #                                                  athlete_id=123456,
    #                                                  dataframe=mock_dataframe)
    # db_activity = DBActivity(
    #     activity_id=activity.id,
    #     user_id=dbutil_admin.get_user_id_by_name("JohnTest")[0],
    #     athlete_id=activity.athlete_id,
    #     pickle=activity.pickle()
    # )
    #
    # dbutil_admin.add_activity(db_activity)


@pytest.fixture(scope='function')
def test_user_id():
    return dbutil_admin.get_user_id_by_name("JohnTest")[0]


@pytest.fixture(scope='function')
def mock_activity():
    mock_dataframe = dbutil.read_dataframe_from_csv()
    activity = CyclingActivityFactory().get_activity(id=999999,
                                                     name="Bike Ride",
                                                     athlete_id=123456,
                                                     dataframe=mock_dataframe)
    return activity


def test_get_user(populate_db, test_user_id):
    # testing existing user
    user = dbutil.get_user(test_user_id)
    assert isinstance(user, Users)
    assert user.username == "JohnTest"

    # testing non-existing user
    user = dbutil.get_user(153)
    assert user is None


def test_get_strava_athlete_id_and_token(populate_db, test_user_id):
    user_id, token = dbutil.get_strava_athlete_id_and_token(test_user_id)
    assert user_id == 123456
    assert token == "token"
    assert dbutil.get_strava_athlete_id_and_token(150) is None


def test_get_athlete_info(populate_db, test_user_id):
    info = dbutil.get_athlete_info(test_user_id)
    assert info == "info"
    assert dbutil.get_athlete_info(150) is None


def test_store_new_activity(populate_db, test_user_id, create_db_connection, mock_activity):
    dbutil._store_new_activity(user_id=test_user_id,
                               athlete_id=123456,
                               activity_id=999999,
                               pickle=mock_activity.pickle())

    with create_db_connection as connection:
        select = connection.execute(f"SELECT * FROM db_activity").fetchall()

    assert len(select) == 1
    assert select[0].activity_id == 999999
    assert select[0].user_id == test_user_id
    assert select[0].athlete_id == 123456
    assert isinstance(select[0].pickle, memoryview)


def test_store_new_duplicate_activity(populate_db, test_user_id, create_db_connection, mock_activity):
    with pytest.raises(dbutil.DuplicateActivity):
        dbutil._store_new_activity(user_id=test_user_id,
                                   athlete_id=123456,
                                   activity_id=999999,
                                   pickle=mock_activity.pickle())


def test_get_activity_from_db(populate_db):
    activity = dbutil.get_activity_from_db(activity_id=999999)
    assert isinstance(activity, bytes)


def test_update_user(populate_db, test_user_id):
    # check correct update
    update = {'strava_athlete_info': 'new_info',
              'strava_access_token': 'new_token'}
    dbutil.update_user(user_id=test_user_id, update=update)

    assert dbutil.get_athlete_info(user_id=test_user_id) == 'new_info'

    # attempt update non-existent user
    with pytest.raises(dbutil.UserDoesNotExist):
        update = {'strava_athlete_info': 'new_info',
                  'strava_access_token': 'new_token'}
        dbutil.update_user(user_id=155, update=update)


def test_store_activity(populate_db, test_user_id):
    # Test string (updating) existing activity
    stored_activity = DBActivity.query.filter_by(activity_id=999999).first()
    stored_pickle = stored_activity.pickle

    mock_dataframe = dbutil.read_dataframe_from_csv()
    activity_update = CyclingActivityFactory().get_activity(id=999999,
                                                            name="Updated Bike Ride",
                                                            athlete_id=123456,
                                                            dataframe=mock_dataframe)
    dbutil.store_activity(user_id=test_user_id,
                          athlete_id=123456,
                          activity_id=999999,
                          pickle=activity_update.pickle())

    updated_activity = DBActivity.query.filter_by(activity_id=999999).first()
    updated_pickle = updated_activity.pickle
    assert updated_activity.pickle != stored_pickle
    assert Activity.from_pickle(updated_pickle).name == "Updated Bike Ride"

    # Test string new activity
    new_activity = CyclingActivityFactory().get_activity(id=888888,
                                                         name="New Activity",
                                                         athlete_id=123456,
                                                         dataframe=mock_dataframe)
    dbutil.store_activity(user_id=test_user_id,
                          athlete_id=123456,
                          activity_id=888888,
                          pickle=new_activity.pickle())

    new_activity = DBActivity.query.filter_by(activity_id=888888).first()
    assert Activity.from_pickle(new_activity.pickle).id == 888888
    assert Activity.from_pickle(new_activity.pickle).name == "New Activity"


def test_delete_activity(populate_db, test_user_id, create_db_connection):
    mock_dataframe = dbutil.read_dataframe_from_csv()
    activity_update = CyclingActivityFactory().get_activity(id=777777,
                                                            name="777777",
                                                            athlete_id=123456,
                                                            dataframe=mock_dataframe)
    dbutil.store_activity(user_id=test_user_id,
                          athlete_id=123456,
                          activity_id=777777,
                          pickle=activity_update.pickle())

    dbutil.delete_activity(user_id=test_user_id, activity_id=777777)

    with create_db_connection as connection:
        activities = connection.execute(f"SELECT * FROM db_activity").fetchall()

    ids = [activity.activity_id for activity in activities]
    assert 777777 not in ids


def test_get_user_id_by_activity_id(populate_db, test_user_id):
    # test function providing existing activity
    user_id = dbutil.get_user_id_by_activity_id(activity_id=999999)
    assert user_id == test_user_id
    # test function providing non-existing activity
    user_id = dbutil.get_user_id_by_activity_id(activity_id=555555)
    assert user_id is None


def test_read_dataframe_from_csv():
    df = dbutil.read_dataframe_from_csv()
    assert isinstance(df, pandas.DataFrame)
