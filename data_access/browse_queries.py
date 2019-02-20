import os
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate,\
    Inhibitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_access.display_tables import Kinase_results

dbpath = os.path.join('database', 'PhosphoQuest.db')
engine = create_engine(f'sqlite:///{dbpath}')

Base.metadata.bind = engine
DBsession = sessionmaker()

def browse_subcat(category):
    """Function to give subcategories results """
    # TODO finish switch function work out categories for substrates/inhibitors
    tabledict = {'Kinase': [Kinase, {'Family':Kinase.kin_family,
                        'Cellular_Location': Kinase.kin_cellular_location}]
                 }
                 #'Substrate': [Substrate,
                 #'Inhibitor': Inhibitor}

    table, field = category.split("-")
    #get database field for query
    #dbtable = tabledict[table][0]
    dbfield = tabledict[table][1][field]
    session = DBsession()

    #___TEMPORARY FORCE TO GENE FOR DISPLAY PURPOSES~~~~
    dbfield = Kinase.kin_gene
    subcats = []
    #run query for all distinct reuslts from table and field name
    s = session.query(dbfield.distinct()).all()
    # for item in s:
    #     subcats.append(item[0])
    print(type(s))
    return s


def browse_link(link):
    """ function to take link and display results"""
    #will split link and query for matches in appropriate table
    pass

def searchexact(text, table, fieldname):
    """ Test universal exact search function for table/field name"""
    session = DBsession()
    results = session.query(table).filter(fieldname == text).all()
    # check if query has returned results
    if results:
        session.close()
        return results

    else:
        session.close()
        return ['No results found']

def kin_detail(text):
    """function to do something with kinase url thing
     and show individual item."""

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

#
# def query_to_dfhtml(query_results, table, link_col = None, drop_cols = None):
#     """ Function to parse query output to pandas dataframe for selected columns
#      and create html for website. Link Col and drop cols are optional"""
#
#     # get attribute names for this table
#     colnames = table.__table__.columns.keys()
#     datalist = {}
#
#     for col in colnames:
#         if col not in drop_cols:
#         # only parse info for wanted columns
#             if col in headers:
#                 # find human friendly column header
#                 header = headers[col]
#                 datalist[header] = []
#                 for item in query_results:
#                     datalist[header].append(getattr(item, col))
#
#             else:
#                 datalist[col] = []
#                 # if human friendly version not available
#                 for item in query_results:
#                     datalist[col].append(getattr(item, col))
#
#         else:
#             continue
#
#     df = pd.DataFrame.from_dict(datalist)
#
#     if link_col != None:
#         link_col2 = headers[link_col]# translate link col
#         df[link_col2] = df[link_col2].apply(
#             lambda x: '<a href="{{url_for(f"/browse_detail/{link_col}">\
#                         link_col2</a>')
#     df = df.to_html(index=False)
#     return df

def query_to_list(query_results, table, drop_atrs):
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
            if name not in drop_atrs:  # check not dropped
                if name in headers:
                    header = headers[name]  # translate to human readable
                    x = (header, getattr(item, name))
                    resultlist.append(x)
                else:
                    x = (name, getattr(item, name))
                    resultlist.append(x)
            else:
                continue  # pass over if in drop_attrs
        result.append(resultlist)

    return result

