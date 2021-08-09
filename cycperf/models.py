#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from cycperf import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    strava_id = db.Column(db.Integer, unique=True)
    strava_scope = db.Column(db.Text)
    strava_access_token = db.Column(db.String(40))
    strava_token_expires_at = db.Column(db.DateTime(timezone=False))
    strava_refresh_token = db.Column(db.String(40))
    strava_athlete_info = db.Column(db.JSON)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class DBActivity(db.Model):
    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    athlete_id = db.Column(db.Integer, db.ForeignKey('user.strava_id'), nullable=False)
    json = db.Column(db.JSON)
    laps = db.Column(db.JSON)
    streams = db.Column(db.JSON)
    df_json = db.Column(db.JSON)
    intervals = db.Column(db.JSON)
    blob = db.Column(db.BLOB)
    comment = db.Column(db.Text)


class DBDataFrame(db.Model):
    activity_id = db.Column(db.Integer, db.ForeignKey('db_activity.activity_id'), primary_key=True, nullable=False)
    df_json = db.Column(db.JSON)
