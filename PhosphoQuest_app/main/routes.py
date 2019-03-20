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
    """render documentation pages"""

    if doc == "database":
        return render_template('documentation_database.html', title="Database_content")

    elif doc == "analysis":
        return render_template('documentation_analysis.html', title="Analysis")

    elif doc == "browse":
        return render_template('documentation_browse.html', title="Browse_search")

    else:
     return render_template('documentation_main.html', title='Documentation')


@main.route("/about")
def about():
    """render home page"""
    return render_template('about.html', title='About_us')

