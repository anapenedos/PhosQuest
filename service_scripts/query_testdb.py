import sys
import os
#so we can access the scripts..
sys.path.insert(0, 'data_access')
from sqlalchemy_declarative import Kinase, Substrate, Inhibitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dbpath = os.path.join('database', 'kinases_test3_all.db')
engine = create_engine(f'sqlite:////{ dbpath }')

Kinase.metadata.bind = engine
DBsession = sessionmaker()
DBsession.bind = engine
session = DBsession

session.query(Kinase).all()

