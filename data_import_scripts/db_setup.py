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

# --------------------------------------------------------------------------- #
# project imports
# import the base class
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base, Kinase, \
    Substrate, Inhibitor

# import PhosphoSitePlus, MRC Inhibitor and BindingDB file parsers
from data_import_scripts.table_parsing import kin_sub_import, \
    phos_sites_import, dis_sites_import, reg_sites_import, bdb_inhib_import, \
    mrc_inhib_import

# import data frame import to database function
from data_import_scripts.sqlalchemy_import import import_data_from_data_frame

# import API import functions and function to get primary key values from table
from data_import_scripts.api_import import get_uniprot_api_data, \
    get_pubchem_api_data, get_table_values_for_search

# import data frame heading: (Class, 'class_attribute') dictionaries
from data_import_scripts.df_to_attributes import kin_sub_human_to_class, \
    phos_sites_human_to_class, reg_sites_human_to_class, \
    dis_sites_human_to_class, mrc_inhib_source_to_class, \
    bindingDB_human_to_class, uniprot_kin_to_class, uniprot_subs_to_class, \
    pubchem_to_class

# import session maker function
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession

# =========================================================================== #

# Create database tables/schema if not present
# Create engine that stores schema in the database directory
# PhosphoQuest.db file.
# The echo flag sets up SQLAlchemy logging
db_path = os.path.join('database', 'PhosphoQuest.db')
engine = create_engine('sqlite:///' + db_path, echo=True)
# Create all tables
Base.metadata.create_all(engine)


# =========================================================================== #

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
# import_data_from_data_frame(kin_sub_human, kin_sub_human_to_class)
# import_data_from_data_frame(phos_sites_human, phos_sites_human_to_class)
# import_data_from_data_frame(reg_sites_human, reg_sites_human_to_class)
# import_data_from_data_frame(dis_sites_human, dis_sites_human_to_class)
# import_data_from_data_frame(mrc_inhib_source, mrc_inhib_source_to_class)
#
# # --------------------------------------------------------------------------- #
# # filter BindingDB data frame so that it contains only inhibitors of existing
# # kinases in the kinases table
# kinases_in_table = get_table_values_for_search(Kinase)
#
# # filter BindingDB df based on existing kinases in DB
# filtered_bdb_df = bindingDB_human[
#     bindingDB_human['UniProt_(SwissProt)_Primary_ID_of_Target_Chain']\
#         .isin(kinases_in_table)]
#
# # import filtered BindingDB data into DB
# import_data_from_data_frame(filtered_bdb_df, bindingDB_human_to_class)
#
# # =========================================================================== #
# # Manual data curating
#
# # Inhibitor InChI key stored in InChI field as well
# # open a SQLite session
session = create_sqlsession()
# inh_to_correct = session.query(Inhibitor).filter(
#     Inhibitor.inhib_pubchem_cid == 9549284).first()
# inh_to_correct.inhib_int_chem_id = 'InChI=1S/C16H12F3N3S/c17-16(18,' \
#                                    '19)14-4-2-1-3-12(14)13(9-20)15(22)' \
#                                    '23-11-7-5-10(21)6-8-11/h1-8H,21-22H2/' \
#                                    'b15-13+'

# --------------------------------------------------------------------------- #
# Inhibitor PubChem SID in place of CID; CID already in DB
inh_to_del = session.query(Inhibitor).filter(
    Inhibitor.inhib_pubchem_cid == 160968186).first()
session.delete(inh_to_del)

session.commit()
session.close()

# =========================================================================== #
# # API imports
#
# # Add kinase cellular location, full name and family to kinases table
# # get needed data from uniprot
# kin_uniprot_data = get_uniprot_api_data(Kinase)
# # import data into database
# import_data_from_data_frame(kin_uniprot_data, uniprot_kin_to_class)
#
# # df1 = kin_uniprot_data[kin_uniprot_data['Entry'] == 'Q9Y478']
# # import_data_from_data_frame(df1, uniprot_kin_to_class)

# --------------------------------------------------------------------------- #
# Add substrate full name to DB using Uniprot API
subs_uniprot_data = get_uniprot_api_data(Substrate)
# import data into database
import_data_from_data_frame(subs_uniprot_data, uniprot_subs_to_class)

# --------------------------------------------------------------------------- #

# Add inhibitors full name to inhibitors table
# get needed data from PubChem
inhib_pubchem_data = get_pubchem_api_data(Inhibitor)
# import data into database
import_data_from_data_frame(inhib_pubchem_data, pubchem_to_class)