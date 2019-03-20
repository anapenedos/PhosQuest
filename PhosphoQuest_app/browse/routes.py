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
    """ route to create details from browse ,render template with triple
     results,   kinase detail + tables of phosphosites and inhibitors"""

    #Run kinase detail query
    results = browse_queries.browse_detail(text, 'Kinase')

    # run related phosphosites query
    phos = browse_queries.kin_phos_query(text)

    #run related inhibitors query
    inh = browse_queries.kin_inhib_query(text)


    return render_template('search_results.html', title="Kinase",
                           style="triple", results=results, table= phos,
                           related="Phosphosites", table2 = inh,
                           related2="Inhibitors", text=text)

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
                           style='double', results=results, table=table,
                           related="Phosphosites", text=text)


@browse.route("/phosites_detail/<text>")
def phosites_detail(text):
    """
    create detail view output of phosphosites by accession.
    :param text: string of phos group ID
    :return: template
    """
    results = browse_queries.browse_detail(text,'Phosphosite')
    table = browse_queries.phos_kin_query(text)

    return render_template('search_results.html', title="Phosphosite",
                           style='double', results=results, table=table,
                           related="Kinases", text=text)

@browse.route("/inh_detail/<text>")
def inh_detail(text):
    " inhibitor detail sets up for adding pubchem widget"
    results = browse_queries.browse_detail(text, 'Inhibitor')
    table = browse_queries.inhib_kin_query(text)
   # cid = results[0][0][1]  # get pubchem CID from results to pass

    return render_template('search_results.html', title="Inhibitor",
                           style="double", results=results, cid=text, text=text,
                           table=table, related="Targeted Kinases")
