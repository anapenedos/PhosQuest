from flask import render_template, Blueprint
import browse_queries

browse = Blueprint('browse', __name__)

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
        'Kinase': ['Kinase-Family', 'Kinase-Cellular_Location'],
        'Substrate': ['Substrate-category1', 'Substrate-category2',
                      'Substrate-category3'],
        'Inhibitor': ['Inhibitor-category1', 'Inhibitor-category2',
                      'Inhibitor-category3']
    }

    if category in categories: # if this is the first specific category level
        links = categories[category]

        return render_template('browse_cat.html', title="Browse", links=links,
                               cat="cat", category=category)

    else: # if this is the subcategory level (requiring query)

        links = browse_queries.browse_subcat(category)
        return render_template('browse_cat.html', title="Browse",
                               links=links, cat="subcat",category=category)


@browse.route("/browse_table/<subcategory>")
def browse_table(subcategory):
    """ route to create table format for browse results in subcategory"""
    table = browse_queries.browse_table(subcategory)
    return render_template('browse_table.html', title=subcategory, table=table)

# TODO write specific detail routes as table link does NOT contain table info

@browse.route("/kin_detail/<text>")
def kin_detail(text):
    """ route to create details"""
# add funciton to search for other info here
    return render_template('404_error.html', title="Browse")

@browse.route("/sub_detail/<text>")
def sub_detail(text):
   """ route to create details"""
   # add funciton to search for other info here
   return render_template('404_error.html', title="Browse")

