from flask import Flask, render_template, url_for, redirect
from test_data import browse_data
from forms import RegistrationForm, LoginForm, UploadForm
from werkzeug.utils import secure_filename
import os

# create instance of FLASK class. __name__ is name of module.
app = Flask(__name__)

# security for site secret key generated in python using secrets module
# token hex method
app.config['SECRET_KEY'] = '7302b128c277227526063af5c73ec426'


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
    """render template with browse data and title for browse page"""
    return render_template('browse.html', browse_data=browse_data,
                           title="Search")


# route for browse page with browse template
@app.route("/search",methods=['GET', 'POST'])
def search():
    """render template with browse data and title for browse page"""
    return render_template('search.html', title="Search")


# route for upload page with file handling method
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Create upload route"""
    form = UploadForm()
    save_dir = "/temp_upload_directory"
    if form.validate_on_submit():
        f = form.data_file.data
        filename = "uploaded_"+ secure_filename(f.filename)
        f.save(os.path.join('temp_upload_directory',filename))

        #This is where we could call the processing modules
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form)


# route for browse page with browse template
@app.route("/results")
def results():
    """render template with analysis results page"""
    return render_template('results.html', title='results')

# Test route for now may or may not want in final site??
@app.route("/register", methods=['GET', 'POST'])
def register():
    """Create instance of register form"""
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


# Test route for now may or may not want in final site??
@app.route("/login",methods=['GET', 'POST'])
def login():
    """ Create instance of register form """
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)




# if run from python directly run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
