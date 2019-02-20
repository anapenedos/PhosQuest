from flask import flash, render_template, Blueprint
from data_access import query_db
from PhosphoQuest_app.search.forms import SearchForm

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
        #Currently just searching on Kinase NAME field only.
        flash(f'You searched for "{search_txt}"\
            in {search_table} {search_option} using {search_type} match',
              'info')
        # call query switch function to decide which search and display option
        results, style = query_db.query_switch(search_txt, search_type,
                                                 search_table, search_option)
        return render_template('search_results.html', title="Search results",
                               results=results, style=style)
    else:

        return render_template('search.html', title="Search", form=form)



