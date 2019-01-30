# Standard library imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate

# Create engine that stores data in the local directory's
# kinases_test.db file.
db_path = os.path.join('database', 'test_db.db')
engine = create_engine(f'sqlite:///{ db_path }')
# Bind the engine to the metadata of the base class so that the
# classes can be accessed through a DBSession instance
Base.metadata.bind = engine

# DB session to connect to DB and keep any changes in a "staging zone"
DBSession = sessionmaker(bind=engine)
session = DBSession()

# TODO loop over dataframe to instantiate mini / full DBs

session.add_all([
    Kinase(kin_acc_num='AA00001', kin_name='Kinase 1', kin_gene='KIN1',
           kin_loc='cytoplasm', kin_fam='family 1'),
    Kinase(kin_acc_num='AA00002', kin_name='Kinase 2', kin_gene='KIN2',
           kin_loc='nucleous', kin_fam='family 1'),
    Kinase(kin_acc_num='AA00003', kin_name='Kinase 3', kin_gene='KIN3',
           kin_loc='nucleous', kin_fam='family 2'),
    Kinase(kin_acc_num='AA00004', kin_name='Kinase 4', kin_gene='KIN4',
           kin_loc='cytoplasm', kin_fam='family 3'),
    Kinase(kin_acc_num='AA00005', kin_name='Kinase 5', kin_gene='KIN5',
           kin_loc='cytoplasm', kin_fam='family 3'),
    Substrate(subs_acc_num='SU00001', subs_name='Substrate 1',
              subs_gene_id='S001', subs_gene='SUB1', subs_prot='Sub1',
              subs_genomic_loc='1q23h',
              subs_mod_res='T', subs_domain='domain 1', subs_ab='XX-0001'),
    Substrate(subs_acc_num='SU00002', subs_name='Substrate 2',
              subs_gene_id='S002', subs_gene='SUB2', subs_prot='Sub2',
              subs_genomic_loc='1q23h',
              subs_mod_res='S', subs_domain='domain 1', subs_ab='XX-0002'),
    Substrate(subs_acc_num='SU00003', subs_name='Substrate 3',
              subs_gene_id='S003', subs_gene='SUB3', subs_prot='Sub3',
              subs_genomic_loc='1q23h',
              subs_mod_res='T', subs_domain='domain 2', subs_ab='XX-0003'),
    Substrate(subs_acc_num='SU00004', subs_name='Substrate 4',
              subs_gene_id='S004', subs_gene='SUB4', subs_prot='Sub4',
              subs_genomic_loc='1q23h',
              subs_mod_res='S', subs_domain='domain 1', subs_ab='XX-0004'),
    Substrate(subs_acc_num='SU00005', subs_name='Substrate 5',
              subs_gene_id='S005', subs_gene='SUB5', subs_prot='Sub5',
              subs_genomic_loc='1q23h',
              subs_mod_res='T', subs_domain='domain 2', subs_ab='XX-0005')])


# commit all changes
session.commit()