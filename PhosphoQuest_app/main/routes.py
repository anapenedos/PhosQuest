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
    return render_template('documentation_main.html', title='Documentation')

@main.route("/documentation/<doc>")
def documentation_category(doc):
    """render documentation page"""
    if doc == "":
        return render_template('documentation_main.html', title="Main")

    elif doc == "analysis":
        return render_template('documentation_analysis.html', title="Analysis")

    else:
     return render_template('documentation_main.html', title='Documentation')


@main.route("/about")
def about():
    """render home page"""
    return render_template('about.html', title='About_us')

