import sys
import os

#so we can access the scripts..
sys.path.insert(0, 'data_access')
from sqlalchemy_declarative import Base, Kinase, Substrate, Inhibitor,\
            Phosphosite, Location
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, attributes

def querytest():
    """ query entire test db into lists of info from all tables """
    #create db path using os to avoid problems with windows vs linux
    dbpath = os.path.join('database', 'kinases_test3_all.db')
    engine = create_engine(f'sqlite:///{ dbpath }')
    Base.metadata.bind = engine
    DBsession = sessionmaker()
    DBsession.bind = engine
    session = DBsession()

    #get first result from DB
    #convert to dict and remove first key (object instance)
    kinase  = session.query(Kinase).first()
    substrate  = session.query(Substrate).first()
    inhibitor  = session.query(Inhibitor).first()
    phosphosite  = session.query(Phosphosite).first()
    location  = session.query(Location).first()

    result = [kinase, substrate, inhibitor, phosphosite, location]

    return result