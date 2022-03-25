from market.app import db, app
from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.models import *
from market.forms import RegisterForm, LoginForm, Itemform, HotelForm
import json
from flask_login import login_user, logout_user, login_required, current_user

user_bp = Blueprint('user_bp', __name__, template_folder='templates')

@user_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('restaurant_bp.market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('user/register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('restaurant_bp.market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('user/login.html', form=form)


@user_bp.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@user_bp.route('/getuser/<user_id>', methods=['GET', 'POST'])
def getuser_page(user_id):
    data = {}
    try:
        u = User.query.filter_by(id=user_id).first()
        print(u)
        if u is not None:
            data['username'] = u.username
            data['email'] = u.email_address
            data['budget'] = u.budget
            data['query_status'] = 200
        else:
            data['query_status'] = 404
    except Exception:
        data['query_status'] = 500
    return data