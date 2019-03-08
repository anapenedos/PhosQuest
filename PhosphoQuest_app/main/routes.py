from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)

# create route for home page works with / and /home page address
# uses home html template
@main.route("/")
@main.route("/home")
def home():
    """render home page"""
    return render_template('home.html', title='home')

# app route for documentation page
@main.route("/documentation")
def documentation():
    """render documentation page"""
    return render_template('documentation.html', title='Documentation')