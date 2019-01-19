"""Test form for login with password"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileRequired

"""Set up forms classes and required fields
we need to add email in here if we actually use this code."""


class RegistrationForm(FlaskForm):
    """Registration form class"""
    username = StringField('username',
                           validators = [DataRequired(),
                                       Length(min=2, max=30)])
    password = PasswordField('password', validators = [DataRequired()])
    password_confirm = PasswordField('confirm_password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])

    submit = SubmitField("Create login")


class LoginForm(FlaskForm):
    """Login form Class"""
    username = StringField('username',
                           validators = [DataRequired(),
                                       Length(min=2, max=30)])
    password = PasswordField('password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class UploadForm(FlaskForm):
    """Upload data form class"""
    data_file = FileField(validators=[FileRequired()])
    submit = SubmitField("Upload")