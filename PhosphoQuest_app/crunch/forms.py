
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    """Upload data form class with file type validator"""
    data_file = FileField('Upload data file for processing',
                          validators=[FileAllowed(['csv', 'tsv', 'txt']),
                                      FileRequired()])
    report_options = [('sig','Significant hits only'),
                      ('full','Full Report Table')]

    select = SelectField('Choose result format', choices=report_options)

    submit = SubmitField("Upload")