from PhosphoQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Inhibitor, Phosphosite
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.interface_dicts import headers
from PhosphoQuest_app.data_access import display_tables

# create table dictionary to translate table name for search queries
tabledict = {'kinase': Kinase, "phosphosite":Phosphosite,'substrate':Substrate,
                 'inhibitor':Inhibitor}


def query_switch(text,type, table, option):
    """
    function to switch between different query methods
    based on the inputs from the website search interface options
    :param text: search text (string)
    :param type: query type ('exact' or 'like')
    :param table: database table ('kinase', 'substrate' or 'inhibitor')
    :param option: search field ('acc_no' or 'name')
    :return: query result object and string representing style of output
                'list', 'table', or 'None' and 'cid' if for inhibitor
    """
    #find right field to search based on selected table and name or acc_no
    fielddict = {'kinase': [Kinase.kin_accession, Kinase.kin_full_name],
                 'substrate': [Substrate.subs_accession,
                               Substrate.subs_full_name],
                 'inhibitor': [Inhibitor.inhib_pubchem_cid,
                               Inhibitor.inhib_name]}
    print(text,type,table,option)

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
        results,style = format_results(results,table)

    else:
        results = searchlike(text, dbtable, field)
        results, style = format_results(results, table)
    return results, style

def format_results(results, table):
    """
    Function to format query results for display depending on number of results
    :param results: query output
    :param table: table class object
    :return: styled query results, style variable
    """
    #output different styles of results depending on number of results
    if 'No results found' in results:
        style = 'None'

    elif len(results) < 2: # if only 1 results display as list
        results = query_to_list(results, table)
        style = 'list'

    else:
        style ='table'
        # if more results display as table for each type
        if table == 'kinase':
            results = display_tables.Kinase_results(results)
        elif table == 'inhibitor':
            # make short name up to 30 characters to avoid long table
            results = display_tables.Inhibitor_results(results)
        else:
            results = display_tables.Substrate_results(results)

    return results, style


def searchlike(text, table, fieldname):
    """
    Universal LIKE search function for table/field name,returns all fields
    :param text: search text (string)
    :param table: db table class object
    :param fieldname: dbtable field object
    :return: query results
    """
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
    """
    Universal exact search function for table/field name
    :param text: search text (string)
    :param table: db table class object
    :param fieldname: dbtable field object
    :return: query results
    """
    session = create_sqlsession()
    results = session.query(table).filter(fieldname == text).all()
    session.close()
    # check if query has returned results
    if results:
        return results
    else:
        return ['No results found']

def all_table(table):
    """
    Function to return all results from one db table
    :param table: dbtable object
    :return: query output
    """
    session = create_sqlsession()
    results = session.query(table).all()
    session.close()
    # check if query has returned results
    if results:
        return results
    else:
        return ['No results found']




def query_to_list(query_results, table):
    """
    Function to parse query output to list of lists for selected attributes
      for website (results <3). Creates links for some values
    :param query_results: query object
    :param table: Table Class object
    :return: list containing list of tuples for each attribute for each result
    """

    # get attribute names for this table
    names = table.__table__.columns.keys()
    # initialise result list

    resultlist = []
    # iterate through query results checking for names and dropped attrs
    for item in query_results:
        result = []
        for name in names:
            # set attribute variable from query output based on name
            attrib = getattr(item, name)
            if name in headers:
                # translate to human readable
                header = headers[name]
            else:
                header = name

            # pass if value is 'None'
            if attrib == None:
                continue
            x = (header, attrib)

            # Add tuple to result list
            result.append(x)

        #add result to result list
        resultlist.append(result)

    return resultlist


