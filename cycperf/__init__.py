#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask.helpers import get_root_path
from flask_login import login_required

import dash_bootstrap_components as dbc

from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from cycperf.main.routes import main
    from cycperf.users.routes import users
    # from flaskblog.posts.routes import posts
    # from flaskblog.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    # app.register_blueprint(posts)
    # app.register_blueprint(errors)
    # app.register_blueprint(simple_dash)

    register_dash(app)

    return app


def register_dash(app):
    from cycperf.dashapp.layout import layout
    from cycperf.dashapp.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dash_app = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/application/',
                         external_stylesheets=[dbc.themes.BOOTSTRAP],
                         assets_folder=get_root_path(__name__) + 'dashboard/assets/',
                         meta_tags=[meta_viewport])

    with app.app_context():
        dash_app.title = 'application'
        dash_app.layout = layout
        register_callbacks(dash_app)

    _protect_dashviews(dash_app)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])

