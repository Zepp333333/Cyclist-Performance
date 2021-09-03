#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import datetime
import json

import pandas
import pandas as pd
import pytest

from hardio.models import DBActivity, Users
from iobrocker import dbutil, dbutil_admin
from iobrocker.utils import CustomEncoder, CustomDecoder
from logic import Activity, CyclingActivityFactory




@pytest.fixture(scope='function')
def mock_activity2():
    df = dbutil.read_dataframe_from_csv()
    with open('tests/testing_data/test_activity.json', 'r') as infile:
        activity_json = json.load(infile)

    athlete_id = activity_json['athlete']['id']
    date = datetime.datetime.strptime(activity_json['start_date'], '%Y-%m-%d %H:%M:%S%z')
    activity_id = 999999
    activity_name = "activity2"
    activity = CyclingActivityFactory().get_activity(
        id=activity_id,
        athlete_id=athlete_id,
        name=activity_name,
        date=date,
        dataframe=df,
        details=json.dumps(activity_json, default=str)
    )
    return activity


@pytest.fixture
def store_call_parameters(mock_activity, test_user_id):
    return {
        'user_id': test_user_id,
        'athlete_id': mock_activity.athlete_id,
        'activity_id': mock_activity.id,
        'date': mock_activity.date,
        'details': mock_activity.details,
        'name': mock_activity.details['name'],
        'dataframe': mock_activity.dataframe.to_json(),
        'laps': '',
        'intervals': json.dumps(mock_activity.intervals, cls=CustomEncoder, indent=4)
    }


@pytest.fixture
def store_call_parameters2(mock_activity2, test_user_id):
    return {
        'user_id': test_user_id,
        'athlete_id': mock_activity2.athlete_id,
        'activity_id': mock_activity2.id,
        'date': mock_activity2.date,
        'details': mock_activity2.details,
        'name': mock_activity2.name,
        'dataframe': mock_activity2.dataframe.to_json(),
        'laps': '',
        'intervals': json.dumps(mock_activity2.intervals, cls=CustomEncoder, indent=4)
    }


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
    assert user_id == 21932478
    assert token == "token"
    assert dbutil.get_strava_athlete_id_and_token(150) is None


def test_get_athlete_info(populate_db, test_user_id):
    info = dbutil.get_athlete_info(test_user_id)
    assert info == "info"
    assert dbutil.get_athlete_info(150) is None


def test_store_new_activity(populate_db, test_user_id, create_db_connection, store_call_parameters):
    dbutil._store_new_activity(**store_call_parameters)

    with create_db_connection as connection:
        select = connection.execute(f"SELECT * FROM db_activity").fetchall()

    assert len(select) == 1
    assert select[0].activity_id == 5806863104
    assert select[0].user_id == test_user_id
    assert select[0].athlete_id == 21932478
    assert "Whole Activity" in select[0].intervals


def test_store_new_duplicate_activity(populate_db, store_call_parameters):
    with pytest.raises(dbutil.DuplicateActivity):
        dbutil._store_new_activity(**store_call_parameters)


def test_get_activity_from_db(populate_db, test_user_id):
    activity = dbutil.get_activity_from_db(user_id=test_user_id, activity_id=5806863104)
    assert isinstance(activity, DBActivity)


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


def test_store_activity(populate_db, test_user_id, mock_activity, mock_activity2, store_call_parameters, store_call_parameters2):
    # Test string (updating) existing activity
    stored_activity = DBActivity.query.filter_by(activity_id=5806863104).first()

    params = {'user_id': test_user_id,
              'athlete_id': mock_activity.athlete_id,
              'activity_id': mock_activity.id,
              'date': mock_activity.date,
              'details': mock_activity.details,
              'dataframe': pd.DataFrame().to_json(),
              'name': mock_activity.name,
              'laps': '',
              'intervals': []}

    dbutil.store_activity(**params)

    updated_activity = DBActivity.query.filter_by(activity_id=5806863104).first()
    assert updated_activity.intervals == []

    # Test string new activity
    dbutil.store_activity(**store_call_parameters2)

    new_activity = DBActivity.query.filter_by(activity_id=999999).first()
    assert new_activity.activity_id == 999999


def test_delete_activity(populate_db, test_user_id, create_db_connection):
    dbutil.delete_activity(user_id=test_user_id, activity_id=999999)

    with create_db_connection as connection:
        activities = connection.execute(f"SELECT * FROM db_activity").fetchall()

    ids = [activity.activity_id for activity in activities]
    assert 999999 not in ids


def test_get_user_id_by_activity_id(populate_db, test_user_id):
    # test function providing existing activity
    user_id = dbutil.get_user_id_by_activity_id(activity_id=5806863104)
    assert user_id == test_user_id
    # test function providing non-existing activity
    user_id = dbutil.get_user_id_by_activity_id(activity_id=555555)
    assert user_id is None


def test_read_dataframe_from_csv():
    df = dbutil.read_dataframe_from_csv()
    assert isinstance(df, pandas.DataFrame)
