from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from .models import Hospital, Appointment
from .extensions import db
from flask_login import login_required, current_user
from datetime import datetime

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def home():
    # Landing - maybe list hospitals
    hospitals = Hospital.query.all()
    return render_template('index.html', hospitals=hospitals)

@main_bp.route('/<hospital_slug>')
@login_required
def index(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    # Basic access control: ensure user belongs to hospital
    if current_user.hospital_id != hosp.id:
        abort(403)
    # show today's appointments
    today = datetime.utcnow().date()
    appts = Appointment.query.filter(
        Appointment.hospital_id == hosp.id
    ).order_by(Appointment.scheduled_at.asc()).limit(50).all()
    return render_template('dashboard.html', hospital=hosp, appointments=appts)