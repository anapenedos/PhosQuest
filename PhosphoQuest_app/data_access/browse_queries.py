from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base, Kinase,\
    Substrate, Inhibitor

from PhosphoQuest_app.data_access.display_tables import Kinase_first_results, \
    Substrate_first_results, Inhibitor_first_results
from PhosphoQuest_app.data_access.query_db import searchlike, \
    searchexact,all_table
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.interface_dicts import headers,\
    location_cats, kin_family_cats


# TODO finish categories for substrates/inhibitors#
tabledict = {'Kinase': [Kinase, {'Family': Kinase.kin_family,
                    'Cellular_Location': Kinase.kin_cellular_location},
                        Kinase.kin_accession],
             'Substrate':[Substrate,
                          {'All':Substrate,
                           'Chromosome_Location':
                               Substrate.subs_chrom_location},
                          Substrate.subs_accession]

             }


def browse_subcat(category):
    """Function to give subcategories results """
    table, field = category.split("~")
    #get database field for query
    dbfield = tabledict[table][1][field]

    # Use query output or curated categories depending on which field etc.
    if table == 'Kinase' and field == 'Cellular_Location':
        return location_cats

    elif table == 'Kinase' and field == 'Family':
        return kin_family_cats

    elif table == 'Substrate' and field =='All':
        results = browse_substrates()
        return results

    # run query for all distinct results from table and field name
    else:
        session = create_sqlsession()
        subcats = session.query(dbfield.distinct()).all()
        links =[subcat[0] for subcat in subcats if subcat[0] != None]
        #remove forward and black slash that cause problems in links
        return links



def browse_table(subcategory):
    """ function to take subcategory and display results as flask_table"""
    #catch inhibitors that skip levels.
    if subcategory == 'Inhibitor':
        out_table = browse_inhibitors()
        return out_table

    # perform database query for other subcategories
    else:
        table, field, text = subcategory.split("~")

        #return all results for Substrate~All results


        #get database field for query
        dbtable = tabledict[table][0]
        dbfield = tabledict[table][1][field]
        #translate any slash characters passed in link
        text = text.replace("&F&","/")
        text = text.replace("&B&","\\")

        # run query for all  results from table and field name for input text
        results = searchlike(text, dbtable, dbfield)

        #find table format for output
        if 'No Results Found' not in results:
            if table == 'Kinase':
                out_table = Kinase_first_results(items=results)

            elif table =='Substrate':
                out_table = Substrate_first_results(items=results)

            return out_table


        else:
            return results


def browse_inhibitors():
    """ function to return all inhibitors as FLask table"""
    results = all_table(Inhibitor)
        #find table format for output
    if 'No Results Found' not in results:
        for item in results:
            #make short name up to 20 characters
            item.inhib_short_name = item.inhib_short_name[:20]
        out_table = Inhibitor_first_results(items=results)
        return out_table
    else:
        return results

def browse_substrates():
    """ function to return all inhibitors as FLask table"""
    results = all_table(Substrate)
        #find table format for output
    if 'No Results Found' not in results:
        out_table = Substrate_first_results(items=results)
        return out_table
    else:
        return results


def browse_detail(text, table):
    """function to do and show individual item detail from link."""
    if table == 'Inhibitor':
        dbtable = Inhibitor
        dbfield = Inhibitor.inhib_pubchem_cid
    else:
        dbtable = tabledict[table][0]
        dbfield = tabledict[table][2]

    results = searchexact(text, dbtable, dbfield)
    results = query_to_list(results, dbtable)
    return results





def query_to_list(query_results, table):
    """ Function to parse query output to list of lists for selected attributes
      for website (results <4). Allows to drop some attributes"""

    # get attribute names for this table
    names = table.__table__.columns.keys()
    # initialise result list
    result = []
    # iterate through query results checking for names and dropped attrs
    for item in query_results:
        resultlist = []
        for name in names:

            if name in headers:
                header = headers[name]  # translate to human readable
                x = (header, getattr(item, name))
                resultlist.append(x)
            else:
                x = (name, getattr(item, name))
                resultlist.append(x)

        result.append(resultlist)

    return result

