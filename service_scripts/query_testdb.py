import sys
import os
#so we can access the scripts..
sys.path.insert(0, 'data_access')
from sqlalchemy_declarative import Base, Kinase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create db path using os to avoid problems with windows vs linux
dbpath = os.path.join('database', 'kinases_test3_all.db')
engine = create_engine(f'sqlite:///{ dbpath }')
Base.metadata.bind = engine
DBsession = sessionmaker()
DBsession.bind = engine
session = DBsession()

kinase  = session.query(Kinase).all()

for item in kinase:
    print("Kinase is " + item.kin_name + "\t Kinase Family is " + item.kin_fam)

