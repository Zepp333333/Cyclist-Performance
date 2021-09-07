#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
"""
HARDIO application lets you connect to to your profile at
Strava.com, download activities and perform extensive analysis with emphasis on
cycling activities and unique intent to enable post-interval recovery analysis on similar
workouts.

Module utilises Flask to run application, enable user management and authorization, as well as
app authorization with Strava. Plotly/Dash is run under Flask to enable authorized access.
"""

import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask.helpers import get_root_path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_required
from flask_mail import Mail
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config) -> Flask:
    """
    Instantiates Flask app together with required objects (db, flask-migrate, login_manager etc). Registers routes and
    Dash application.
    :return: instance of Flask app including registered Dash app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate.init_app(app, db)
    # with app.app_context():
    #     upgrade()

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from hardio.main.routes import main
    from hardio.users.routes import users
    # todo import errors.handlers

    app.register_blueprint(main)
    app.register_blueprint(users)
    # todo app.register_blueprint(errors)

    register_dash(app)

    return app


def register_dash(app: Flask) -> None:
    """
    Registers Dash application under provided Flask app.
    :param app: Instance of Flask app
    :return: None
    """
    from hardio.dashapp.layout import layout
    from hardio.dashapp.callbacks import register_callbacks
    from hardio.dashapp.interval_callbacks import register_interval_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dash_app = dash.Dash(__name__,
                         server=app,
                         title='HARDIO',
                         url_base_pathname='/application/',
                         external_stylesheets=[dbc.themes.BOOTSTRAP],
                         assets_folder=get_root_path(__name__) + 'dashboard/assets/',
                         meta_tags=[meta_viewport])

    # dash_app.enable_dev_tools(dev_tools_ui=True,
    #                           dev_tools_serve_dev_bundles=True, )
    with app.app_context():
        dash_app.layout = layout
        register_callbacks(dash_app)
        register_interval_callbacks(dash_app)

    _protect_dash_views(dash_app)


def _protect_dash_views(dash_app: dash.Dash) -> None:
    """
    Protects Dash application views byt requiring login
    :param dash_app: instance of Dash app to protect views for
    :return:
    """
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
