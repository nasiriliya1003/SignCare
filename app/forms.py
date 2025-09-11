from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length

class CreateUserForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=64)]
    )
    email = StringField(
        "Email (optional)",
        validators=[Email(), Length(max=120)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    role = SelectField(
        "Role",
        choices=[("staff", "Staff"), ("doctor", "Doctor"), ("patient", "Patient"), ("admin", "Admin")],
        default="staff",
        validators=[DataRequired()]
    )
    submit = SubmitField("Create User")

class BookAppointmentForm(FlaskForm):
    patient_name = StringField(
        "Your Full Name",
        validators=[DataRequired(), Length(min=2, max=128)]
    )
    patient_contact = StringField(
        "Contact (phone/email)",
        validators=[Length(max=64)]
    )
    scheduled_at = DateTimeLocalField(
        "Preferred Date & Time",
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )
    submit = SubmitField("Book Appointment")