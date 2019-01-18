from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo

#set up registration form class and required fields
class RegistrationForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('password',validators=DataRequired())
    password_confirm = PasswordField('confirm_password',validators=[DataRequired(),EqualTo('password')])

