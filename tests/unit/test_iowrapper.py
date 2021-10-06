#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import pytest
from iobrocker import dbutil, IO
import dill
from logic import Activity


class TestIowrapper:

    def test_build_mock_up_ride(self):
        assert False

    def test_get_athlete_info(self):
        assert False

    def test_get_list_of_activities(self):
        assert False

    def test_get_strava_activities(self):
        assert False

    def test__build_activity(self):
        assert False

    def test_get_hardio_activity_by_id(self, test_user_id, test_client, mock_activity):
        io = IO(test_user_id, token_refresh=False)
        io.save_activity(mock_activity)
        activity = io.get_hardio_activity_by_id(5806863104)
        assert isinstance(activity, Activity)
        assert activity.id == 5806863104
        assert isinstance(activity.dataframe, pd.DataFrame)

    def test_save_activities(self):
        assert False

    def test_save_activity(self, test_user_id, test_client, mock_activity, create_db_connection):
        io = IO(test_user_id, token_refresh=False)
        io.save_activity(mock_activity)
        with create_db_connection as connection:
            select = connection.execute(f"SELECT * FROM db_activity").fetchall()

        assert select[0].activity_id == 5806863104
        assert select[0].user_id == test_user_id
        assert select[0].athlete_id == 21932478
        assert "All" in select[0].intervals[0]

    def test_delete_activity_by_id(self):
        assert False

    def test_get_strava_activity_by_id(self):
        assert False

    def test_get_last_activity(self):
        assert False

    def test_is_strava_authorized(self):
        assert False

    def test_is_strava_token_expired(self):
        assert False

    def test_refresh_token(self):
        assert False

    def test_build_activity(self, test_user_id, test_client):
        with open('tests/testing_data/detailed_activity.dill', 'rb') as f:
            strava_activity = dill.load(f)
        io = IO(test_user_id, token_refresh=False)
        activity = io.make_hardio_activity_from_strava_activity(strava_activity=strava_activity.to_dict(),
                                                                get_streams=False)
        assert isinstance(activity, Activity)
        assert isinstance(activity.details, dict)
