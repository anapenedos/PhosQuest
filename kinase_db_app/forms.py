"""Test form for login with password"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
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


class LoginForm(FlaskForm):
    """Login form Class"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")



class UploadForm(FlaskForm):
    """Upload data form class with file type validator"""
    data_file = FileField('Upload data file for processing',
                          validators=[FileAllowed(['csv','tsv'])])
    submit = SubmitField("Upload")