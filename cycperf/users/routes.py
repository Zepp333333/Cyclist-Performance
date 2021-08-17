#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

"""
Users blueprint for the application
"""

from typing import Union

from flask import (render_template, url_for, flash,
                   redirect, Blueprint, request)
from flask_login import login_user, current_user, logout_user, login_required

from cycperf import db, bcrypt
from cycperf.models import Users
from cycperf.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                 RequestResetForm, ResetPasswordForm)
from cycperf.users.utils import save_picture, send_reset_email
from iobrocker import strava_auth

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register() -> Union[str, redirect]:
    """
    Register route
    :return: rendered registration template or redirect to login
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login() -> Union[str, redirect]:
    """
    Login route
    :return: rendered login template or redirect next or home page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout() -> redirect:
    """
    Logout route
    :return: rendered home template
    """
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account() -> Union[str, redirect]:
    """
    Account Route
    :return: rendered account template or redirects to account_template in case of POST request (eventually modified)
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# todo implement account delete

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request() -> Union[str, redirect]:
    """
    Password reset request route
    :return: rendered reset_request template or login if user is not logged in
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token: str) -> Union[str, redirect]:
    """
    Password reset token verification route
    :param token:
    :return: rendered reset_token template or reset request template if token invalid
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Users.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/strava_login")
@login_required
def strava_login() -> redirect:
    """
    strava_login route
    :return: redirects user to strava.com for app authorization
    """
    return redirect(strava_auth.prep_app_auth_url())
# todo consider the scenario if user creates new account in CP and tries to authorize already authorized strava account
    # currently it leads to sqlalchemy.exc.IntegrityError


@users.route("/exchange_token")
@login_required
def strava_return() -> redirect:
    """
    Return route from strava.com authorization procedure. Intended to capture authorization results as scopes
    :return: redirects to application if authorization successful or to strava_login if not
    """
    if strava_auth.check_strava_auth_return(request.args):
        athlete = strava_auth.retrieve_strava_athlete(auth_code=request.args['code'])
        current_user.strava_id = athlete['id']
        db.session.commit()
        return redirect(url_for('/application/'))
    else:
        return redirect(url_for('users.strava_login'))
