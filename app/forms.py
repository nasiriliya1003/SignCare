from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

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
        "Patient Full Name*",
        validators=[DataRequired(), Length(min=2, max=128)]
    )
    
    patient_email = StringField(
        "Email",
        validators=[Optional(), Email(), Length(max=120)],
        render_kw={"placeholder": "patient@example.com"}
    )
    
    patient_phone = StringField(
        "Phone Number*",
        validators=[DataRequired(), Length(max=15)],
        render_kw={"placeholder": "+250 7XX XXX XXX", "required": "true"}
    )
    
    district = SelectField(
        "District/Region*",
        choices=[
            ('', '[Select]'),
            ('Kigali', 'Kigali'),
            ('Nyarugenge', 'Nyarugenge'),
            ('Gasabo', 'Gasabo'),
            ('Kicukiro', 'Kicukiro'),
            ('Other', 'Other')
        ],
        validators=[DataRequired()],
        default=''
    )
    
    scheduled_at = DateTimeLocalField(
        "Preferred Date & Time*",
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local", "required": "true"}
    )
    
    comments = TextAreaField(
        "Additional Comments",
        validators=[Optional(), Length(max=500)],
        render_kw={"placeholder": "Any additional information or special requirements...", "rows": 4}
    )
    
    submit = SubmitField("Book Appointment")