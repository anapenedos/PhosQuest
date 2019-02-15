from flask import flash, render_template, url_for, redirect
from kinase_db_app import app, db, bcrypt
from data_access import query_db
from service_scripts import userdata_display, user_data_crunch
from kinase_db_app.forms import RegistrationForm, LoginForm, UploadForm
from kinase_db_app.forms import SearchForm
from werkzeug.utils import secure_filename
from kinase_db_app.model import User
import traceback

#Create 404 errorhandling route
@app.errorhandler(404)
def page_not_found(e):
    """render special 404 page"""
    return render_template('404_error.html'), 404

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
    #browse_data = query_db.allbrowse()
    browse_data = None
    """render template with browse data and title for browse page"""
    return render_template('browse.html', browse_data=browse_data,
                           title="Browse")

# route for browse page with browse template
@app.route("/search",methods=['GET', 'POST'])
def search():
    """render template with browse data and title for browse page"""
    form = SearchForm()
    #gather form info, text and user selections
    search_txt = form.search.data # user entered text
    search_type = form.select.data # exact or LIKE match
    search_table = form.table.data # data table in DB to search
    search_option = form.option.data # name or accession no

    if search_txt:
        #Currently just searching on Kinase NAME field only.
        flash(f'You searched for "{search_txt}"\
            in {search_table} {search_option} using {search_type} match',
              'info')
        # call query switch function to decide which search and display option
        results, style = query_db.query_switch(search_txt, search_type,
                                                 search_table, search_option)
        return render_template('search_results.html', title="Search results",
                               results=results, style=style)

    else:

        return render_template('search.html', title="Search", form=form)


# route for upload page with file handling method
@app.route('/analysis',methods=['GET', 'POST'])
def analysis():
    """Create upload and analysis route"""
    form = UploadForm()
     #if form validates (correct file types) save file in temp dir
    if form.validate_on_submit():
        try:
            f = form.data_file.data
            filename =  secure_filename(f.filename)
            #run all analyses.
            all_data = userdata_display.run_all(f)
            #selector for type of report (test version)
            if form.select.data == 'full':
                table = user_data_crunch.style_df(all_data['full_sty_sort'])
                # temporary test display bokeh df
                #table = userdata_display.bokeh_df(all_data['full_sty_sort'])


                flash(f'File {filename} successfully analysed', 'success')
                return render_template('results.html',
                            title='All results',
                                    table=table )

            else:

                table = user_data_crunch.\
                         style_df(all_data['parsed_sty_sort'])

                #temporary test display bokeh df
                #table = userdata_display.bokeh_df(all_data['full_sty_sort'])

                flash(f'File {filename} successfully analysed', 'success')

                return render_template('results.html',
                    title='All data', table=table)




        except Exception:
            print(traceback.format_exc())
            flash(f'Error please try again ','danger')
            return render_template('upload.html', form=form, report='upload')

    return render_template('upload.html', form=form, report='upload')


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
