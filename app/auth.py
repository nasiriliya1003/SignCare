from flask import Blueprint, render_template, redirect, url_for, flash, request
from .extensions import db, login_manager
from .models import User, Hospital
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hospital_slug = request.form.get('hospital_slug')
        username = request.form.get('username')
        password = request.form.get('password')

        hospital = Hospital.query.filter_by(slug=hospital_slug).first()
        if not hospital:
            flash("Hospital not found.", "danger")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(username=username, hospital_id=hospital.id).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in.", "success")
            return redirect(url_for('main.index', hospital_slug=hospital.slug))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('auth.login'))

# loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))