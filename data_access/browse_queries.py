import os
from sqlalchemy_declarative import Base, Kinase, Substrate,\
    Inhibitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from display_tables import Kinase_results
from data_access.query_db import headers
dbpath = os.path.join('database', 'PhosphoQuest.db')
engine = create_engine(f'sqlite:///{dbpath}')

Base.metadata.bind = engine
DBsession = sessionmaker()

# TODO finish categories for substrates/inhibitors
tabledict = {'Kinase': [Kinase, {'Family': Kinase.kin_family,
                    'Cellular_Location': Kinase.kin_cellular_location}]
             }


# 'Substrate': [Substrate,
# 'Inhibitor': Inhibitor}


def browse_subcat(category):
    """Function to give subcategories results """

    table, field = category.split("~")
    #get database field for query
    #dbtable = tabledict[table][0]
    dbfield = tabledict[table][1][field]
    session = DBsession()

    # #___TEMPORARY FORCE TO GENE FOR DISPLAY PURPOSES~~~~
    # dbfield = Kinase.kin_gene
    # run query for all distinct reuslts from table and field name
    subcats = session.query(dbfield.distinct()).all()

    links =[subcat[0] for subcat in subcats if subcat[0] != None]

    return links


def browse_table(subcategory):
    """ function to take subcategory and display results as flask_table"""
    table, field, text = subcategory.split("~")
    #get database field for query
    dbtable = tabledict[table][0]
    dbfield = tabledict[table][1][field]

    # # *************force to gene for now**************
    # dbfield = Kinase.kin_gene


    # run query for all distinct reuslts from table and field name
    results = searchexact(text, dbtable, dbfield)
    #find table format for output
    if results != ['No Results Found']:
        if table == 'Kinase':
            out_table = Kinase_results(items=results)
        elif table =='Substrate':
            #out_table =Substrate_results(results)
            pass
        elif table == 'Inhibitor':
            pass

    else:
        pass

    return out_table

def searchexact(text, table, fieldname):
    """ Test universal exact search function for table/field name"""
    session = DBsession()
    results = session.query(table).filter(fieldname == text).all()
    session.close()
    # check if query has returned results
    if results:
        return results

    else:
        return ['No results found']

def kin_detail(text):
    """function to do something with kinase url thing
     and show individual item."""
    # TODO update - decide what detail to show
    results = searchexact(text, Kinase, Kinase.kin_accession)
    return results

def sub_detail(text):
    """function to do something with kinase url thing
     and show individual item."""

    results = searchexact(text, Substrate, Substrate.subs_accession)

    return results


def inh_detail(text):
    """function to do something with kinase url thing
     and show individual item."""

    results = searchexact(text, Inhibitor, Inhibitor.inhib_pubchem_cid)

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

