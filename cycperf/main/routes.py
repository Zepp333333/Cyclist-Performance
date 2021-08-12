from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    content = []
    return render_template('index.html', content=content)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
