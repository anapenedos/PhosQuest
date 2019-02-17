from flask import render_template, Blueprint

browse = Blueprint('browse', __name__)


# TODO work on the browse pages
# route for browse page with browse template


@browse.route("/browse")
def browse_main():
    """render template with browse data and title for browse page"""
    return render_template('browse_main.html', title="Browse")


@browse.route("/browse/<category>")
def browse_cat(category):
    """ Display sub-categories depending on browse main click"""
    # category dict to look up sub categories for browse.
    # TODO decide on categories for display
    categories = {
        'kinase': ['Kinase-Family', 'Kinase-Cellular_Location'],
        'substrate': ['Substrate-category1', 'Substrate-category2',
                      'Substrate-category3'],
        'inhibitor': ['Inhibitor-category1', 'Inhibitor-category2',
                      'Inhibitor-category3']
    }

    if category in categories:
        category_links = categories[category]
        return render_template('browse_cat.html', title="Browse",
                               links=category_links)

    else:
        # TODO make  error page for if someone manually types a subcategory
        # go back to main browse categories if not in dict
        return render_template('browse_main.html', title="Browse")
