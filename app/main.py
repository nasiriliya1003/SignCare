from werkzeug.security import generate_password_hash
from .forms import CreateUserForm
from .models import User, Hospital, Appointment   # added Appointment
from .extensions import db
from flask_login import login_required, current_user
from flask import Blueprint, request, flash, render_template, redirect, url_for, abort
from datetime import datetime

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def home():
    hospitals = Hospital.query.all()
    return render_template('index.html', hospitals=hospitals)


@main_bp.route("/<hospital_slug>/create-user", methods=["GET", "POST"])
@login_required
def create_user(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()

    # only hospital admins can create users
    if current_user.hospital_id != hosp.id or current_user.role not in ("admin",):
        abort(403)

    form = CreateUserForm()

    if form.validate_on_submit():
        # create the user and hash the password
        new_user = User(
            hospital_id=hosp.id,
            username=form.username.data.strip(),
            email=form.email.data.strip() if form.email.data else None,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f"User '{new_user.username}' created successfully.", "success")
        return redirect(url_for("main.view_users", hospital_slug=hosp.slug))

    return render_template(
        "create_user.html",
        form=form,
        hospital=hosp,
        active="create"
    )


@main_bp.route('/<hospital_slug>')
@login_required
def index(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.hospital_id != hosp.id:
        abort(403)

    today = datetime.utcnow().date()
    appts = Appointment.query.filter(
        Appointment.hospital_id == hosp.id
    ).order_by(Appointment.scheduled_at.asc()).limit(50).all()

    return render_template('dashboard.html', hospital=hosp, appointments=appts)


@main_bp.route('/<hospital_slug>/users')
@login_required
def view_users(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.hospital_id != hosp.id:
        abort(403)
    return render_template('view_users.html', hospital=hosp, active='view')


@main_bp.route('/<hospital_slug>/visualization')
@login_required
def visualization(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.hospital_id != hosp.id:
        abort(403)
    return render_template('visualization.html', hospital=hosp, active='viz')