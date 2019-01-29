import os
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate,\
    Inhibitor, Phosphosite, Location
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, attributes

dbpath = os.path.join('database', 'kinases_test3_all.db')
engine = create_engine(f'sqlite:///{dbpath}')
Base.metadata.bind = engine
DBsession = sessionmaker()
DBsession.bind = engine
session = DBsession()

def querytest():
    """ query test db and get first item from each table """
    kinase  = session.query(Kinase).first()
    #substrate  = session.query(Substrate).first()
    #inhibitor  = session.query(Inhibitor).first()
    #phosphosite  = session.query(Phosphosite).first()
    #location  = session.query(Location).first()

    result = [kinase]
    session.close()
    return result

