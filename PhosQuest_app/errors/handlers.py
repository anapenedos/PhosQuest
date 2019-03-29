from flask import Blueprint, render_template

#create blueprint for error handler
errors = Blueprint('errors', __name__)

# Create 404 error handling route
@errors.app_errorhandler(404)
def page_not_found(e):
    """render special 404 page"""
    return render_template('404_error.html'), 404

@errors.app_errorhandler(500)
def server_error(e):
    """render 500 page(server error"""
    return render_template('500_error.html'),500
