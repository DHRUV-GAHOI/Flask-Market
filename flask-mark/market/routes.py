from market.app import db, app
from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.models import *
from market.forms import RegisterForm, LoginForm, Itemform, HotelForm
import json
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
