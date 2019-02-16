from flask import render_template, Blueprint

browse = Blueprint('browse', __name__)

#TODO work on the browse pages
# route for browse page with browse template
@browse.route("/browse")
def browse_db():
    """ Use  query function to populate browse page"""
    #browse_data = query_db.allbrowse()
    browse_data = None
    # Not currently functional
    """render template with browse data and title for browse page"""
    return render_template('browse.html', browse_data=browse_data,
                           title="Browse")
