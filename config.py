#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

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
