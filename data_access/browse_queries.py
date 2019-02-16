import os
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate,\
    Inhibitor, Phosphosite, Disease, DiseaseAlteration, CellularLocation
from sqlalchemy import create_engine

import pandas as pd
dbpath = os.path.join('database', 'PhosphoQuest.db')
engine = create_engine(f'sqlite:///{dbpath}')

Base.metadata.bind = engine
DBsession = sessionmaker()

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

def query_to_dfhtml(query_results, table, drop_cols):
    """ Function to parse query output to pandas dataframe for selected columns
     and create html for website"""

    # get attribute names for this table
    colnames = table.__table__.columns.keys()
    datalist = {}

    for col in colnames:
        if col not in drop_cols:  # only parse info for wanted columns
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

        else:
            continue

    df = pd.DataFrame.from_dict(datalist)
    df = df.to_html(index=False)
    return df


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


    # def allbrowse(table):
    # # #     """ query db and get first item from each table (BROWSE)
    # # #     returns all fields """
    # # #
    # # #     DBsession.bind = engine
    # # #     session = DBsession()
    # # #     query  = session.query(table).paginagete()
    # # #     session.close()
    # # #     browse_data = query_to_df(query,table)
    # # #     return browse_data