from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('User', backref='hospital', lazy=True)
    appointments = db.relationship('Appointment', backref='hospital', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    username = db.Column(db.String(64), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), default='staff')  # 'patient', 'doctor', 'admin', 'staff'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    patient_name = db.Column(db.String(128), nullable=False)
    patient_contact = db.Column(db.String(64), nullable=True)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(32), default='booked')  # booked, called, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)