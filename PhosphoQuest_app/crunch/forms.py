
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    """Upload data form class with file type validator"""
    data_file = FileField('Upload data file for processing',
                          validators=[FileAllowed(['csv', 'tsv', 'txt']),
                          FileRequired()])
    submit = SubmitField("Upload")
    