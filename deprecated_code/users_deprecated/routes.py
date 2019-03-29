from flask import Blueprint
from flask import flash, render_template, url_for, redirect
from PhosQuest_app import bcrypt, db
#from PhosQuest_app.users.forms import RegistrationForm, LoginForm
#from PhosQuest_app.users.model import User

users = Blueprint('users', __name__)

# Register route usersmay or may not want in final site??
@users.route("/register", methods=['GET', 'POST'])
def register():
    """Create instance of register form"""
    form = RegistrationForm()
    #if form validates show flash message
    if form.validate_on_submit():
        #note f method works only python 3.6+ (format in older)
        #hash password
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode(\
            'utf-8')
        #create user and add to users_db
        user = User(email= form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!','success')
        return redirect(url_for('users.login'))#

    return render_template('register.html', title='Register', form=form)


# Test route for now
@users.route("/login",methods=['GET', 'POST'])
def login():
    """ Create instance of login form """
    form = LoginForm()
    if form.validate_on_submit():
        #fake login details to test page
        if form.email.data == "test@test.com" and \
            form.password.data == "password":
            flash(' You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful please retry','danger')

    return render_template('login.html', title='Login', form=form)