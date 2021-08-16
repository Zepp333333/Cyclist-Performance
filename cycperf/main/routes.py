from flask import render_template, Blueprint
from iobrocker import IO
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    content = []
    try:
        user_id = current_user.id
        return render_template('index.html', content=content, title='CP Home',
                               strava_authorized=IO(user_id).is_strava_authorized())
    except AttributeError:
        return render_template('index.html', content=content)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
