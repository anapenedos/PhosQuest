from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base, Kinase, \
    Substrate, Inhibitor, Phosphosite
import pandas as pd
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.interface_dicts import headers
from PhosphoQuest_app.data_access import display_tables

# create table dictionary to translate table name for search queries
tabledict = {'kinase': Kinase, "phosphosite":Phosphosite, 'substrate':Substrate,
                 'inhibitor':Inhibitor}

# create field dictionary to give appropriate field name for search  queries
# accession no in first index, name in second index.
#For Phosphosite there is no name so the field phos.site is used


#dictionary for human friendly attribute names
#TODO finish adding Inhibitors to this dict as will be helpful for other things


def query_switch(text,type, table, option):
    """function to switch between different query methods
    based on the inputs from the website interface options"""
    # TODO update to long name when available for Kinase
    #find right field to search based on selected table and name or acc_no
    #using short name for now until long name avail
    fielddict = {'kinase': [Kinase.kin_accession, Kinase.kin_full_name],
                 'substrate': [Substrate.subs_accession,
                               Substrate.subs_full_name],
                 'inhibitor': [Inhibitor.inhib_pubchem_cid,
                               Inhibitor.inhib_short_name]}

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

    # convert table text to table object to apply to query
    dbtable = tabledict[table]

    #carry out query with exact or like method depending on user choice
    if type == "exact":
        results = searchexact(text, dbtable, field)
        if 'No results found' in results:
            style = 'None'
            return results, style

        elif len(results) < 4: # if only 3 or less results display as list
            results = query_to_list(results, dbtable)
            style = 'list'
            return results, style

        else:
            if table == 'kinase':
                results = display_tables.Kinase_first_results(results)
            elif table == 'inhibitor':
                for item in results: #shorten name
                    item.inhib_short_name = item.inhib_short_name[:20]
                results = display_tables.Inhibitor_first_results(results)
                cid='cid'
            else:
                results = display_tables.Substrate_first_results(results)
            style = 'table'
            return results, style, cid

    else:
        results = searchlike(text, dbtable, field)
        if 'No results found' in results:
            style = 'None'
            return results, style

        elif len(results) < 3: # if only 2 or less results display as list
            results = query_to_list(results, dbtable)
            style = 'list'
            return results, style

        else:
            # if more results display as table for each type
            if table == 'kinase':
                results = display_tables.Kinase_first_results(results)
            elif table == 'inhibitor':
                # make short name up to 20 characters to avoid long table
                for item in results:
                    item.inhib_short_name = item.inhib_short_name[:20]
                results = display_tables.Inhibitor_first_results(results)
            else:
                results = display_tables.Substrate_first_results(results)
            style = 'table'

            return results,style


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

def all_table(table):
    session = create_sqlsession()
    results = session.query(table).all()
    session.close()
    # check if query has returned results
    if results:
        return results
    else:
        return ['No results found']




def query_to_list(query_results, table):
    """ Function to parse query output to list of lists for selected attributes
      for website (results <3)."""

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


# def query_to_dfhtml(query_results, table):
#     """ Function to parse query output to pandas dataframe
#      and create html for website"""
#
#     # get attribute names for this table
#     colnames = table.__table__.columns.keys()
#     datalist = {}
#
#     for col in colnames:
#         # only parse info for wanted columns
#         if col in headers:
#             # find human friendly column header
#             header = headers[col]
#             datalist[header] = []
#             for item in query_results:
#                 datalist[header].append(getattr(item, col))
#
#         else:
#             datalist[col] = []
#             # if human friendly version not available
#             for item in query_results:
#                 datalist[col].append(getattr(item, col))
#
#     df = pd.DataFrame.from_dict(datalist)
#     df = df.to_html(index=False)
#     return df
#
