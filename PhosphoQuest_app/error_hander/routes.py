from flask import Blueprint
from flask import render_template

#create blueprint for error handler
error_handler = Blueprint('error_handler', __name__)

# Create 404 error handling route
@error_handler.errorhandler(404)
def page_not_found(e):
    """render special 404 page"""
    return render_template('404_error.html'), 404