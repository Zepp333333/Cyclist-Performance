#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from iobrocker import dbutil_admin
import sqlalchemy
from datetime import datetime


def test_list_users_with_emtpy_db(test_client):
    assert dbutil_admin.list_users() == ""


def test_add_user(test_client, create_db_connection):
    # Create user via tested function
    dbutil_admin.add_user(username="JohnTest",
                          email="johnsnow@gmail.com",
                          password="Pass@word1",
                          strava_id=123456,
                          strava_access_token="token",
                          strava_token_expires_at=datetime(2001, 11, 23),
                          strava_refresh_token="refresh_token",
                          strava_athlete_info="info")

    with create_db_connection as connection:
        select = connection.execute(f"SELECT * FROM USERS WHERE username='JohnTest'").first()

    assert select.username == "JohnTest"
    assert select.email == "johnsnow@gmail.com"
    assert select.password == "Pass@word1"
    assert select.image_file == "default.jpg"
    assert select.strava_id == 123456
    assert select.strava_access_token == "token"
    assert select.strava_token_expires_at == datetime(2001, 11, 23)
    assert select.strava_refresh_token == "refresh_token"
    assert select.strava_athlete_info == "info"


def test_list_users_with_added_user(test_client):
    assert "JohnTest', 'johnsnow@gmail.com', 'default.jpg'" in dbutil_admin.list_users()


def test_get_user_id_by_name(test_client):
    user_ids = dbutil_admin.get_user_id_by_name("JohnTest")
    assert user_ids == [1]


def test_delete_users_strava_auth_info(test_client, create_db_connection):
    dbutil_admin.delete_users_strava_auth_info(dbutil_admin.get_user_id_by_name("JohnTest")[0])

    with create_db_connection as connection:
        select = connection.execute(f"SELECT * FROM USERS WHERE username='JohnTest'").first()

    assert select.username == "JohnTest"
    assert select.email == "johnsnow@gmail.com"
    assert select.password == "Pass@word1"
    assert select.image_file == "default.jpg"
    assert select.strava_id is None
    assert select.strava_access_token is None
    assert select.strava_token_expires_at is None
    assert select.strava_refresh_token is None
    assert select.strava_athlete_info is None


def test_delete_user(test_client, create_db_connection):
    dbutil_admin.delete_user(dbutil_admin.get_user_id_by_name("JohnTest")[0])

    with create_db_connection as connection:
        select = connection.execute(f"SELECT * FROM USERS WHERE username='JohnTest'").all()

    assert select == []




