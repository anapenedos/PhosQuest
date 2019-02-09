# Standard library imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate,\
    Phosphosite, Disease, DiseaseAlteration, Inhibitor,\
    Location, LocationImage


# Create engine that stores data in the local directory's
# kinases_test.db file.
db_path = os.path.join('database', 'db_lite.db')
engine = create_engine(f'sqlite:///{ db_path }')
# Bind the engine to the metadata of the base class so that the
# classes can be accessed through a DBSession instance
Base.metadata.bind = engine

# DB session to connect to DB and keep any changes in a "staging zone"
DBSession = sessionmaker(bind=engine)
session = DBSession()

# TODO loop over dataframe to instantiate mini / full DBs
# TODO do this bit.... ;-)
#session.add_all(


# commit all changes
session.commit()