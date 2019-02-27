import os
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base, Kinase,\
    Substrate, Inhibitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PhosphoQuest_app.data_access.display_tables import Kinase_first_results, \
    Substrate_first_results
from PhosphoQuest_app.data_access.query_db import headers, create_sqlsession,\
        searchlike, searchexact

# TODO finish categories for substrates/inhibitors#
tabledict = {'Kinase': [Kinase, {'Family': Kinase.kin_family,
                    'Cellular_Location': Kinase.kin_cellular_location},
                        Kinase.kin_accession],
             'Substrate':[Substrate,
                          {'Protein_Type':Substrate.subs_protein_type,
                           'Chromosome_Location':
                               Substrate.subs_chrom_location},
                          Substrate.subs_accession]
       }
# 'Inhibitor': Inhibitor}

# dictionary to force subcategories for cellular location
location_cats = ['Acrosome', 'Axon', 'Caveola','Cell cortex', 'Cell junction',
                 'Cell projection', 'Centriole', 'Centromere', 'Chromosome',
                 'Cilium', 'Cytoplasm', 'Cytoskeleton', 'Cytosol', 'Dendrite',
                 'Endoplasmic reticulum', 'Endosome', 'Extracellular',
                 'Golgi apparatus', 'Lysosome', 'Melanosome', 'Microsome',
                 'Midbody', 'Mitochondrion', 'Nucleus', 'Perinuclear',
                 'PML body', 'Ruffle', 'Sarcolemma', 'Secreted',
                 'Secretory vesicle', 'Spindle', 'Synapse']

def browse_subcat(category):
    """Function to give subcategories results """
    table, field = category.split("~")
    #get database field for query
    dbfield = tabledict[table][1][field]

    if table == 'Kinase' and field == 'Cellular_Location':
        return location_cats

    # run query for all distinct reuslts from table and field name
    else:
        session = create_sqlsession()
        subcats = session.query(dbfield.distinct()).all()
        links =[subcat[0] for subcat in subcats if subcat[0] != None]
        print(links)

        return links



def browse_table(subcategory):
    """ function to take subcategory and display results as flask_table"""
    table, field, text = subcategory.split("~")
    #get database field for query
    dbtable = tabledict[table][0]
    dbfield = tabledict[table][1][field]
    print(text, dbtable, dbfield)

    # run query for all distinct reuslts from table and field name
    results = searchlike(text, dbtable, dbfield)
    print(results)
    #find table format for output
    if 'No Results Found' not in results:
        if table == 'Kinase':
            out_table = Kinase_first_results(items=results)

        elif table =='Substrate':
            out_table = Substrate_first_results(items=results)

        elif table == 'Inhibitor':
            pass

    else:
        return results
    return out_table


def browse_detail(text, table):
    """function to do something with kinase url thing
     and show individual item."""
    # TODO update - decide what detail to show
    dbtable = tabledict[table][0]
    dbfield = tabledict[table][2]

    results = searchexact(text, dbtable, dbfield)
    results= query_to_list(results, dbtable)
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

