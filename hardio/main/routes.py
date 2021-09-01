#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

"""
Main blueprint for application
"""
from flask import render_template, Blueprint
from iobrocker import IO
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
def home() -> str:
    """
    Landing page includes logic to check if user logged in and if app is authorized in Strava to produce relevant experience:
        - Advise to create account for new users
        - Ask to authorize app in strava for existing user (in case not authorized previously)
        - Link to proceed to application for logged-in users with app authorized in strava
    :return: rendered template
    """
    content = []
    try:
        user_id = current_user.id
        return render_template('index.html', content=content, title='CP Home',
                               strava_authorized=IO(user_id).is_strava_authorized())
    except AttributeError:
        return render_template('index.html', content=content)


@main.route("/about")
def about() -> str:
    """
    About page
    :return: rendered template
    """
    return render_template('about.html', title='About')
