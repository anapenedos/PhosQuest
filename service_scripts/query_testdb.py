import os
from data_access.sqlalchemy_declarative import Base, Kinase
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, attributes

dbpath = os.path.join('database', 'test_db.db')
engine = create_engine(f'sqlite:///{dbpath}')
Base.metadata.bind = engine
DBsession = sessionmaker()
DBsession.bind = engine
session = DBsession()

def querytest():
    """ query test db and get first item from each table """
    kinase  = session.query(Kinase).all()
    session.close()
    return kinase

