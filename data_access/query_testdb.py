import os
from data_access.sqlalchemy_declarative import Base, Kinase
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, attributes

dbpath = os.path.join('database', 'test_db.db')
engine = create_engine(f'sqlite:///{dbpath}')
Base.metadata.bind = engine
DBsession = sessionmaker()
DBsession.bind = engine


def querytest():
    """ query test db and get first item from each table """
    session = DBsession()
    kinase  = session.query(Kinase).all()
    session.close()
    return kinase


def searchlike(text, table, fieldname):
    """ Test universal LIKE search function for table/field name"""
    text = '%'+ text + '%'
    session = DBsession()
    results = session.query(table).filter(fieldname\
                                          .like(text)).all()
    #check if query has returned results
    if results != []:
        session.close()
        return results
    else:
        session.close()
        return ['No results found']


def searchexact(text, table, fieldname):
    """ Test universal exact search function for table/field name"""
    session = DBsession()
    results = session.query(table).filter(fieldname == text).all()
    # check if query has returned results
    if results != []:
        session.close()
        return results

    else:
        session.close()
        return ['No results found']