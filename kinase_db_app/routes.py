from flask import flash, render_template, url_for, redirect
from kinase_db_app import app, db, bcrypt
from service_scripts import query_testdb
from service_scripts import userdata_display
from kinase_db_app.forms import RegistrationForm, LoginForm, UploadForm
from kinase_db_app.forms import SearchForm
from werkzeug.utils import secure_filename
from kinase_db_app.model import User
import traceback


# create route for home page works with / and /home page address
# uses home html template
@app.route("/")
@app.route("/home")
def home():
    """render home page"""
    return render_template('home.html', title='home')


# route for browse page with browse template
@app.route("/browse")
def browse():
    """ Use test query function to populate browse page"""
    browse_data = query_testdb.querytest()

    """render template with browse data and title for browse page"""
    return render_template('browse.html', browse_data=browse_data,
                           title="Browse")

# route for browse page with browse template
@app.route("/search",methods=['GET', 'POST'])
def search():
    """render template with browse data and title for browse page"""
    form = SearchForm()
    search_txt = form.search.data
    flash(f'Search for " { search_txt }"', 'info')
    return render_template('search.html', title="Search", form=form)


# route for upload page with file handling method
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    """Create upload and analysis route"""
    form = UploadForm()
    import os
     #if form validates (correct file types) save file in temp dir
    if form.validate_on_submit():
        try:
            f = form.data_file.data
            filename =  secure_filename(f.filename)
            #selector for type of report (test version)
            if form.select.data == 'all':
                all_data = userdata_display.run_all(f, filename)

                flash(f'File {filename} successfully analysed', 'success')
                return render_template('results.html',
                            title='Significant Results',
                                       table = all_data['all_html'])

            elif form.select.data == 'sig':
                #Running everything currently but probably don't need all.
                all_data = userdata_display.run_all(f, filename)

                flash(f'File {filename} successfully analysed', 'success')
                return render_template('results.html', title='All Results',
                                       table=all_data['sig_html'])
            elif form.select.data == 'phm':

                userdata_display.run_all(f, filename)
                file = f"{filename}_parsed_heatmap.png"
                header = "Heatmap of significant phophosites"
                return render_template('heatmap.html', title='heatmap',
                                       image=file, header=header)
            else:

                userdata_display.run_all(f, filename)
                file = f"{filename}_full_heatmap.png"
                header = "Heatmap of all phophosites"
                return render_template('heatmap.html', title='heatmap',
                                       image=file, header=header)

        except Exception:
            print(traceback.format_exc())
            flash(f'Error please try again ','danger')
            return render_template('upload.html', form=form)

    return render_template('upload.html', form=form)


# Test route for now may or may not want in final site??
@app.route("/register", methods=['GET', 'POST'])
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
        return redirect(url_for('login'))#

    return render_template('register.html', title='Register', form=form)


# Test route for now
@app.route("/login",methods=['GET', 'POST'])
def login():
    """ Create instance of login form """
    form = LoginForm()
    if form.validate_on_submit():
        #fake login details to test page
        if form.email.data == "test@test.com" and \
            form.password.data == "password":
            flash(' You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful please retry','danger')

    return render_template('login.html', title='Login', form=form)
