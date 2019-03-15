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
    categories = {
        'Kinase': ['Kinase~Family', 'Kinase~Cellular_Location'],
        'Substrate': ['Substrate~All','Substrate~Chromosome_Location']
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

        if type(links) == list:
            cleansedlinks = []
            # remove forward slashes
            for item in links:
                item = item.replace("/","&F&")
                cleansedlinks.append(item)

            return render_template('browse_cat.html', title="Browse",
                                   links=cleansedlinks, cat="subcat",
                                   category=category)
        else:#catch Substrate~All
            return render_template('browse_table.html',title="Substrate",
                                            table=links)



@browse.route("/browse_table/<subcategory>")
def browse_table(subcategory):
    """ route to create table format for browse results in subcategory"""

    table = browse_queries.browse_table(subcategory)
    return render_template('browse_table.html', title=subcategory,
                                            table=table)

@browse.route("/kin_detail/<text>")
def kin_detail(text):
    """ route to create details from browse"""
    # add function to search for other info her""
    results = browse_queries.browse_detail(text, 'Kinase')
    return render_template('search_results.html', title="Browse", style="list",
                           results=results)

@browse.route("/sub_detail/<text>")
def sub_detail(text):
    """
    create list view output of one substrate by accession.
    :param text: subs-acc no
    :return: template
    """
    #run substrate query
    results = browse_queries.browse_detail(text, 'Substrate')
    #run related phosphosite query
    table = browse_queries.subs_phos_query(text)

    return render_template('search_results.html', title="Substrate",
                           style='subphos', results=results, table=table)

@browse.route("/phosites_detail/<text>")
def phosites_detail(text):
    """
    create detail view output of phosphosites by accession.
    :param text: string of accession
    :return: template
    """
    results = browse_queries.browse_detail(text,'Phosphosite')
    return render_template('search_results.html', title="Phosphosite",
                           style='list', results=results)

@browse.route("/inh_detail/<text>")
def inh_detail(text):
    " inhibitor detail"
    results = browse_queries.browse_detail(text, 'Inhibitor')
    cid = results[0][0][1]  # get pubchem CID from results to pass
    return render_template('search_results.html', title="Inhibitor",
                           style="list", results=results, cid=cid)
