"""Test form for login with password"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from kinase_db_app.model import User

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


class SearchForm(FlaskForm):
    """Basic single search box"""
    search = StringField('Enter search criteria',
                          validators=[])
    submit = SubmitField("Search")

    def validate_email(self, email):
        #custom validation for unique email (check not in db)
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use!')

class UploadForm(FlaskForm):
    """Upload data form class with file type validator"""
    data_file = FileField('Upload data file for processing',
                          validators=[FileAllowed(['csv', 'tsv', 'txt']),
                                      FileRequired()])
    submit = SubmitField("Upload")