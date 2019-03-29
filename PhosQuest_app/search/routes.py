from flask import flash, render_template, Blueprint
from PhosQuest_app.data_access import query_db, browse_queries
from PhosQuest_app.search.forms import SearchForm
search = Blueprint('search', __name__)


# route for browse page with browse template
@search.route("/search",methods=['GET', 'POST'])
def search_db():
    """Call switch function to search database and render results
    in various forms depending on number of results"""
    form = SearchForm()
    #gather form info, text and user selections
    search_txt = form.search.data # user entered text
    search_type = form.select.data # exact or LIKE match
    search_table = form.table.data # data table in DB to search
    search_option = form.option.data # name or accession no

    if search_txt:

        # call query switch function to decide which search and display option
        results, style = query_db.query_switch(search_txt, search_type,
                                               search_table, search_option)

        # Prepare flash message with search options

        flash(f'You searched for "{search_txt}" in {search_table} \
              {search_option} using {search_type} \
                    match.', 'info')

        #for inhibitors, get CID number for PubChem 3D Widget
        if style != 'None':
            if search_table == 'inhibitor':
                #if single result returned find related information
                if style == "list":
                    cid = results[0][0][1]#get pubchem CID from results to pass
                    table = browse_queries.inhib_kin_query(cid)
                    return render_template('search_results.html',
                                    title="Inhibitor", results=results,
                                    style='double', table=table, cid=cid,
                                           related = 'Kinases', text=cid)
                else:
                    return render_template('search_results.html',
                                           title="Inhibitor", results=results,
                                           style='table')

            elif search_table == 'substrate':
                if style == "list":
                    subs_acc_no = results[0][0][1]  # get acc-no from results
                    table = browse_queries.subs_phos_query(subs_acc_no)

                    return render_template('search_results.html',
                                 title="Substrate", results=results,
                                 style='double', table=table, text=subs_acc_no,
                                       related='Phosphosites')
                else:

                    return render_template('search_results.html',
                                           title="Substrate", results=results,
                                           style='table')
            if search_table == 'kinase':
                #if single result returned find related information
                if style == "list":
                    kin_acc_no = results[0][0][1]#get  acc no from results
                    table = browse_queries.kin_phos_query(kin_acc_no)
                    table2 = browse_queries.kin_inhib_query(kin_acc_no)

                    return render_template('search_results.html',
                                    title="Kinase", results=results,
                                    style='triple', table=table, table2=table2,
                                    related='Phosphosites', text=kin_acc_no,
                                           related2='Inhibitors')
                else:
                    return render_template('search_results.html',
                                           title="Kinase", results=results,
                                           style='table')

        else: # return results to be filled it "no results " text
           return render_template('search_results.html', title="Search results",
                        style=style)
    else: #return search template
        return render_template('search.html', title="Search", form=form)



