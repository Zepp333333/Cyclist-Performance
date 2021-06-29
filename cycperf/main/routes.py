from flask import render_template, request, Blueprint
from cycperf.models import User

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    page = request.args.get('page', 1, type=int)
    content = []
    return render_template('index.html', content=content)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
