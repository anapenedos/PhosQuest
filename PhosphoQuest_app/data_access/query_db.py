import os
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base, Kinase, \
    Substrate, Inhibitor, Phosphosite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

def create_sqlsession():
    """Function to create database sessions in any script/function in app"""
    dbpath = os.path.join('database', 'PhosphoQuest.db')
    engine = create_engine(f'sqlite:///{dbpath}')
    Base.metadata.bind = engine
    DBsession = sessionmaker()
    session = DBsession()
    return session


# create table dictionary to translate table name for search queries
tabledict = {'kinase': Kinase, "phosphosite":Phosphosite, 'substrate':Substrate,
                 'inhibitor':Inhibitor}

# create field dictionary to give appropriate field name for search  queries
# accession no in first index, name in second index.
#For Phosphosite there is no name so the field phos.site is used


#dictionary for human friendly attribute names
#TODO finish adding Inhibitors to this dict as will be helpful for other things
headers = {
    'kin_accession':'Accession no', 'kin_short_name':'Short name',
    'kin_full_name' :'Full name', 'kin_gene':'Gene',
    'kin_organism':'Species', 'kin_cellular_location':'Cellular location',
    'kin_family': 'Family', 'subs_accession':'Accession no',
    'subs_short_name':'Short name', 'subs_full_name':'Full name',
    'subs_protein_type':'Protein type',
              'subs_molec_weight_kd':'Molecular weight (kd)',
    'subs_gene':'Gene', 'subs_chrom_location':'Chromosome location',
    'subs_organism':'Species', 'phos_group_id':'Group ID',
    'phos_modified_residue': 'Modified residue','phos_site':'Phosphosite',
    'phos_domain':'Phosphorylation domain',
              'phos_cst_catalog_number':'CST Catalog number',
    'phos_p_function':'Phosphorylation Function',
    'phos_p_processes':'Processes',
        'phos_prot_interactions':'Protein Interactions',
    'other_interactions':'Other interactions',
    'phos_bibl_references':'References','phos_notes':'Notes',
    'phos_in_substrate':'In substrate'
}

def query_switch(text,type, table, option):
    """function to switch between different query methods
    based on the inputs from the website interface options"""
    # TODO update to long name when available for Kinase
    #find right field to search based on selected table and name or acc_no
    #using short name for now until long name avail
    fielddict = {'kinase': [Kinase.kin_accession, Kinase.kin_short_name],
                 'substrate': [Substrate.subs_accession,
                               Substrate.subs_full_name],
                 'inhibitor': [Inhibitor.inhib_pubchem_cid,
                               Inhibitor.inhib_full_name]}

    # find appropriate field to apply and find field object
    if table == 'kinase':
        if option == 'acc_no':
            field = fielddict['kinase'][0]
        else:
            field = fielddict['kinase'][1]

    elif table == 'substrate':
        if option == 'acc_no':
            field = fielddict['substrate'][0]
        else:
            field = fielddict['substrate'][1]

    elif table == 'inhibitor':
        if option == 'acc_no':
            field = fielddict['inhibitor'][0]
        else:
            field = fielddict['inhibitor'][1]
    else:
        print(" an error has occurred")
        # TODO create custom error class for logic errors

    # convert table text to table object to apply to query
    table = tabledict[table]

    #carry out query with exact or like method depending on user choice
    if type == "exact":
        results = searchexact(text, table, field)
        if 'No results found' in results:
            style = 'None'
            return results, style

        elif len(results) < 4: # if only 3 or less results display as list
            results = query_to_list(results, table)
            style = 'list'
            return results, style

        else:
            results = query_to_dfhtml(results, table)
            style = 'dataframe'
            return results, style

    else:
        results = searchlike(text, table, field)
        if 'No results found' in results:
            style = 'None'
            return results, style

        elif len(results) < 4: # if only 3 or less results display as list
            results = query_to_list(results, table)
            style = 'list'
            return results, style

        else: # if more results display as table
            results = query_to_dfhtml(results, table)
            style = 'dataframe'
            return results, style


def searchlike(text, table, fieldname):
    """ Test universal LIKE search function for table/field name,
        returns all fields"""
    text = '%'+ text + '%' # add wildcards for LIKE search
    session = create_sqlsession()
    results = session.query(table).filter(fieldname\
                                          .like(text)).all()
    session.close()
    # check if query has returned results
    if results:
        return results
    else:
        return ['No results found']


def searchexact(text, table, fieldname):
    """ Test universal exact search function for table/field name"""
    session = create_sqlsession()
    results = session.query(table).filter(fieldname == text).all()
    session.close()
    # check if query has returned results
    if results:
        return results
    else:
        return ['No results found']

def query_to_dfhtml(query_results, table):
    """ Function to parse query output to pandas dataframe for selected columns
     and create html for website"""

    # get attribute names for this table
    colnames = table.__table__.columns.keys()
    datalist = {}

    for col in colnames:
        # only parse info for wanted columns
        if col in headers:
            # find human friendly column header
            header = headers[col]
            datalist[header] = []
            for item in query_results:
                datalist[header].append(getattr(item, col))

        else:
            datalist[col] = []
            # if human friendly version not available
            for item in query_results:
                datalist[col].append(getattr(item, col))

    df = pd.DataFrame.from_dict(datalist)
    df = df.to_html(index=False)
    return df


def query_to_list(query_results, table):
    """ Function to parse query output to list of lists for selected attributes
      for website (results <4)."""

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


