#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from cycperf import db
from cycperf.models import Users, DBActivity


def delete_user(user_id: int) -> None:
    user = Users.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()


def delete_users_strava_auth_info(user_id: int) -> None:
    user = Users.query.filder_by(id=user_id).first()
    user.strava_id = None
    user.strava_scope = None
    user.strava_access_token = None
    user.strava_token_expires_at = None
    user.strava_athlete_info = None
    db.session.commit()

def list_users() -> str:
    users = Users.query.all()
    string = "\n".join([u.__str__() for u in users])
    return string
