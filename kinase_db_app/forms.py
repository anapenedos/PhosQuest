"""Test form for login with password"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    SelectField, RadioField
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
    """Search form with selectors"""
    search = StringField('Enter Search text',
                          validators=[])
    #Dropdown selector for exact or like match
    options= [('like', 'similar matches'),('exact', 'exact matches')]
    select = SelectField('Choose search type: ', choices=options)

    #radio button selector for table to search
    criteria =[
        ('kinase', 'Kinases'), ('substrate','Substrates'),
        ('inhibitor','Inhibitors')]

    table = RadioField('Search by: ', choices=criteria, default='kinase')

    fields = [('acc_no', 'Accession or ID'), ('name', 'Name')]

    option = RadioField('Search in: ', choices=fields, default='acc_no')

    submit = SubmitField("Search")



class UploadForm(FlaskForm):
    """Upload data form class with file type validator"""
    data_file = FileField('Upload data file for processing',
                          validators=[FileAllowed(['csv', 'tsv', 'txt']),
                                      FileRequired()])
    report_options = [('sig','Significant hits only'),
                      ('full','Full Report Table')]

    select = SelectField('Choose result format', choices=report_options)

    submit = SubmitField("Upload")
