
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
#from PhosphoQuest_app.users.model import User

"""Set up forms classes and required fields
we need to add email in here if we actually use this code."""


class RegistrationForm(FlaskForm):
    """Registration form class"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators = [DataRequired()])
    password_confirm = PasswordField('Confirm password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])

    submit = SubmitField("Create login")

    def validate_email(self, email):
        #custom validation for unique email (check not in db)
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use!')


class LoginForm(FlaskForm):
    """Login form Class"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")
