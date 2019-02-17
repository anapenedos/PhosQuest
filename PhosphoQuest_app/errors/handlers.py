from flask import Blueprint, render_template

#create blueprint for error handler
errors = Blueprint('errors', __name__)

# TODO add 500 errorhandler (Server error)

# Create 404 error handling route
@errors.app_errorhandler(404)
def page_not_found(e):
    """render special 404 page"""
    return render_template('404_error.html'), 404