from flask import render_template, Blueprint
from PhosphoQuest_app.data_access import browse_queries
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
        'Kinase': ['Kinase~Family', 'Kinase~Cellular_Location'],
        'Substrate': ['Substrate~Protein_Type',
                      'Substrate~Chromosome_Location']
    }

    # if this is the first specific category level the category variable
    # will be in the dict if not split variable for category level.
    if category in categories:
        links = categories[category]

        return render_template('browse_cat.html', title="Browse", links=links,
                               cat="cat", category=category)

    elif category == 'Inhibitor':

        table = browse_queries.browse_inhibitors()

        return render_template('browse_table.html', title=category,
                               table=table)

    else: # if this is the subcategory level (requiring query)
        links = browse_queries.browse_subcat(category)
        cleansedlinks = []
        # remove forward slashes
        for item in links:
            item = item.replace("/","&F&")
            cleansedlinks.append(item)

        return render_template('browse_cat.html', title="Browse",
                               links=cleansedlinks, cat="subcat",
                               category=category)


@browse.route("/browse_table/<subcategory>")
def browse_table(subcategory):
    """ route to create table format for browse results in subcategory"""

    table = browse_queries.browse_table(subcategory)
    return render_template('browse_table.html', title=subcategory,
                                            table=table)

# TODO write specific template for browse detail page.
@browse.route("/kin_detail/<text>")
def kin_detail(text):
    """ route to create details from browse"""
    # add function to search for other info her""
    results = browse_queries.browse_detail(text, 'Kinase')
    return render_template('search_results.html', title="Browse", style="list",
                           results=results)

@browse.route("/sub_detail/<text>")
def sub_detail(text):
   """ route to create details"""
   results = browse_queries.browse_detail(text, 'Substrate')

   return render_template('search_results.html', title="Browse", style="list",
                         results=results)

@browse.route("/inh_detail/<text>")
def inh_detail(text):
    """ route to create details from browse"""
    # add function to search for other info her""
    results = browse_queries.browse_detail(text, 'Inhibitor')
    return render_template('search_results.html', title="Browse", style="list",
                           results=results)
