"""
Script to setup SQLite database using
- SQLalchemy declarative schema (data_access\sqlalchemy_declarative.py)
- Data set files parsing functions (data_import_scripts\db_parsing.py)
- Dictionaries mapping data frame headings to class and attributes
  (data_import_scripts\df_to_attributes.py)
- SQLalchemy import script to import parsed data frames into SQLite DB
  (data_import_scripts\sqlalchemy_import.py)

Sets up DB PhosphoQuest.db in database directory.
"""

# =========================================================================== #
# python library imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --------------------------------------------------------------------------- #
# project imports
# import the base class
from data_access.sqlalchemy_declarative import Base, Inhibitor

# import PhosphoSitePlus, MRC Inhibitor and BindingDB file parsers
from data_import_scripts.table_parsing import kin_sub_import, \
    phos_sites_import, dis_sites_import, reg_sites_import, bdb_inhib_import, \
    mrc_inhib_import

# import data frame import to database function
from data_import_scripts.sqlalchemy_import import import_data_from_data_frame

# import data frame heading: (Class, 'class_attribute') dictionaries
from data_import_scripts.df_to_attributes \
    import kin_sub_human_to_class, phos_sites_human_to_class, \
    reg_sites_human_to_class, dis_sites_human_to_class, \
    mrc_inhib_source_to_class, bindingDB_human_to_class

# =========================================================================== #

# Create database tables/schema if not present
# Create engine that stores schema in the database directory
# PhosphoQuest.db file.
# The echo flag sets up SQLAlchemy logging
db_path = os.path.join('database', 'PhosphoQuest.db')
engine = create_engine('sqlite:///' + db_path, echo=True)
# Create all tables
Base.metadata.create_all(engine)


# --------------------------------------------------------------------------- #

### Call functions for data files (in db_source_data) import

# Human kinase/substrate db as data frame.
kin_sub_human = kin_sub_import()

# Human phospho-site db as data frame.
phos_sites_human = phos_sites_import()

# Human disease-site db as data frame.
dis_sites_human = dis_sites_import()

# Human regulatory-site db as data frame.
reg_sites_human = reg_sites_import()

# Human BindingDB as data frame.
bindingDB_human = bdb_inhib_import()

# MRC inhibitor as data frame
mrc_inhib_source = mrc_inhib_import()

# --------------------------------------------------------------------------- #

# Import data from data frames to SQLite database
print('Starting kinase/phosphosite data import. This may take some minutes.')
import_data_from_data_frame(kin_sub_human, kin_sub_human_to_class)
print('Completed kinase/phosphosite data set import.')

print('Starting phosphosite/substrate data import. This may take a couple of '
      'hours.')
import_data_from_data_frame(phos_sites_human, phos_sites_human_to_class)
print('Completed phosphosite/substrate data set import.')

print('Starting regulatory sites data import. This may take some minutes.')
import_data_from_data_frame(reg_sites_human, reg_sites_human_to_class)
print('Completed regulatory sites data set import.')

print('Starting disease alterations data import. This may take some minutes.')
import_data_from_data_frame(dis_sites_human, dis_sites_human_to_class)
print('Completed disease alterations data set import.')

print('Starting MRC inhibitors data import. This may take some minutes.')
import_data_from_data_frame(mrc_inhib_source, mrc_inhib_source_to_class)
print('Completed MRC inhibitors data set import.')

print('Starting BindingDB inhibitors data import. This may take some minutes.')
import_data_from_data_frame(bindingDB_human, bindingDB_human_to_class)
print('Completed BindingDB inhibitors data set import.')

# --------------------------------------------------------------------------- #

# Manual data curating
# Inhibitor InChI key stored in InChI field as well

db_path = os.path.join('database', 'PhosphoQuest.db')
engine = create_engine('sqlite:///' + db_path)
# Bind the engine to the metadata of the base class so that the
# classes can be accessed through a DBSession instance
Base.metadata.bind = engine
# DB session to connect to DB and keep any changes in a "staging zone"
DBSession = sessionmaker(bind=engine)
# open a SQLite session
session = DBSession()
inh_to_correct = session.query(Inhibitor).filter(
    Inhibitor.inhib_pubchem_cid == 9549284).first()
inh_to_correct.inhib_int_chem_id = 'InChI=1S/C16H12F3N3S/c17-16(18,' \
                                   '19)14-4-2-1-3-12(14)13(9-20)15(22)' \
                                   '23-11-7-5-10(21)6-8-11/h1-8H,21-22H2/' \
                                   'b15-13+'
session.commit()
session.close()
