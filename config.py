#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    STRAVA_AUTH_URL = os.environ.get('STRAVA_AUTH_URL')
    STRAVA_APP_CLIENT_ID = int(os.environ.get('STRAVA_APP_CLIENT_ID'))
    STRAVA_APP_CLIENT_SECRET = os.environ.get('STRAVA_APP_CLIENT_SECRET')
    STRAVA_APP_REDIRECT_URI = os.environ.get('STRAVA_APP_REDIRECT_URI')

    STRAVA_TOKEN_EXCHANGE_URL = "https://www.strava.com/oauth/token"

    STRAVA_REQUIRED_SCOPES = ['read', 'read_all', 'profile:read_all', 'activity:read_all', 'activity:write']

    PRIORITIZED_STREAMS: dict[str:int] = {
        'watts': 0,
        'pace': 0,
        'watts30': 2,
        'heartrate': 4,
        'cadence': 6,
        'altitude': 8,
        'velocity_smooth': 10,
        'distance': 12,
        'grade_smooth': 14,
        'temp': 16,
        'moving': 30,
        'latlng': 40,
        'time': 50
    }

    TEST_USER_ID = 1

class ConfigTest:
    TEST_DB_NAME = 'hardio_test_db'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
    TEST_DATABASE_SERVER = 'postgresql://postgres@localhost'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/hardio_test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    STRAVA_AUTH_URL = os.environ.get('STRAVA_AUTH_URL')
    STRAVA_APP_CLIENT_ID = int(os.environ.get('STRAVA_APP_CLIENT_ID'))
    STRAVA_APP_CLIENT_SECRET = os.environ.get('STRAVA_APP_CLIENT_SECRET')
    STRAVA_APP_REDIRECT_URI = os.environ.get('STRAVA_APP_REDIRECT_URI')

    STRAVA_TOKEN_EXCHANGE_URL = "https://www.strava.com/oauth/token"

    STRAVA_REQUIRED_SCOPES = ['read', 'activity:read_all', 'profile:read_all']

    TEST_USER_ID = 1
