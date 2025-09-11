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

# Doctor routes
@main_bp.route('/<hospital_slug>/summaries')
@login_required
def view_summaries(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "doctor":
        abort(403)
    summaries = []  # TODO: fetch structured summaries
    return render_template('summaries.html', hospital=hosp, summaries=summaries, active='summaries')

@main_bp.route('/<hospital_slug>/appointments')
@login_required
def appointments_dashboard(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "doctor":
        abort(403)
    appts = []  # TODO: fetch doctor appointments
    return render_template('appointments.html', hospital=hosp, appointments=appts, active='appointments')

@main_bp.route('/<hospital_slug>/notify/<int:patient_id>', methods=['POST'])
@login_required
def notify_patient(hospital_slug, patient_id):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "doctor":
        abort(403)

    patient = User.query.get_or_404(patient_id)

    # Example: simulate sending notification
    flash(f"Notification sent to {patient.username}", "success")

    return redirect(url_for("main.index", hospital_slug=hosp.slug))

# Admin routes
@main_bp.route('/<hospital_slug>/triage')
@login_required
def triage_overview(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "admin":
        abort(403)
    triage_data = []  # TODO: fetch queue distribution
    return render_template('triage.html', hospital=hosp, triage=triage_data, active='triage')

@main_bp.route('/<hospital_slug>/booking-settings')
@login_required
def booking_settings(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "admin":
        abort(403)
    return render_template('booking_settings.html', hospital=hosp, active='booking')

# Staff routes
@main_bp.route('/<hospital_slug>/register-patient', methods=['GET', 'POST'])
@login_required
def register_patient(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "staff":
        abort(403)
    # TODO: implement registration form
    return render_template('register_patient.html', hospital=hosp, active='register')

@main_bp.route('/<hospital_slug>/record-symptoms', methods=['GET', 'POST'])
@login_required
def record_symptoms(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "staff":
        abort(403)
    # TODO: implement symptom capture form
    return render_template('record_symptoms.html', hospital=hosp, active='symptoms')

@main_bp.route('/<hospital_slug>/queue')
@login_required
def manage_queue(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "staff":
        abort(403)
    # TODO: display/manage patient queue
    return render_template('queue.html', hospital=hosp, active='queue')

# Manager / IT routes
@main_bp.route('/<hospital_slug>/deployment')
@login_required
def deployment_settings(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "manager":
        abort(403)
    return render_template('deployment.html', hospital=hosp, active='deploy')

@main_bp.route('/<hospital_slug>/status')
@login_required
def system_status(hospital_slug):
    hosp = Hospital.query.filter_by(slug=hospital_slug).first_or_404()
    if current_user.role != "manager":
        abort(403)
    status_info = {}  # TODO: fetch system health metrics
    return render_template('status.html', hospital=hosp, status=status_info, active='status')