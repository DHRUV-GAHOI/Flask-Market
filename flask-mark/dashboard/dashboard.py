from market.app import db, app
from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.models import *
from market.forms import RegisterForm, LoginForm, Itemform, HotelForm
import json
from flask_login import login_user, logout_user, login_required, current_user


dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard_page():
    
    dash = Dashboard.query.filter_by(id=1).first()
    if dash is None:
        dash = Dashboard()
        db.session.add(dash)
        db.session.commit()
        # print(dash.user_fail, dash.user_success)
    # else:
    #     print(dash.user_fail, dash.user_success)
    if request.method == 'POST':
        # print(request.get_json(), 'data')
        data = request.get_json()
        if data['hit_url'] == 'getuser':
            if data['hit_status']: dash.user_success += 1
            else: dash.user_fail += 1
        elif data['hit_url'] == 'getitem':
            if data['hit_status']: dash.item_success += 1
            else: dash.item_fail += 1 
        elif data['hit_url'] == 'gethotel':
            if data['hit_status']: dash.hotel_success += 1
            else: dash.hotel_fail += 1 
        elif data['hit_url'] == 'getorder':
            if data['hit_status']: dash.order_success += 1
            else: dash.order_fail += 1
            
        db.session.commit()
            
    
    return render_template('dashboard/dashboard.html', dashboard=dash) 