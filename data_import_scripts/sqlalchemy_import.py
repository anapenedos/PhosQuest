# Standard library imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Project imports
# classes and join tables
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate, \
    Phosphosite, Disease, DiseaseAlteration, Inhibitor, Location, \
    kinases_inhibitors_table, kinases_phosphosites_table
# data import dataframes
from data_import_scripts.db_parsing import kin_sub_human, \
    phos_sites_human, reg_sites_human, dis_sites_human, mrc_inhib_source
# dataframe headings to class attribute dictionaries
from data_import_scripts.dataframes_to_attributes import kin_sub_human_to_class


# def add_update_info
#
# def
# def get_primary_key_values (df_row, key_list)
#
# def is_in_table
#
# def create_relationships

def import_kinase_substrate_data(kin_sub_dataframe): #[Kinase, Substrate, Phosphosite]
    """
    Takes in dataframe storing kinase substrate info and populates relevant
    entries in SQLite database.

    :param kin_sub_dataframe: pandas dataframe from PhosphositePlus import (df)
    """
    # Create engine that stores data to database\<file_name>.db
    # TODO replace db file by the final db name
    db_path = os.path.join('database', 'PhosphoQuest.db')
    engine = create_engine('sqlite:///' + db_path)
    # Bind the engine to the metadata of the base class so that the
    # classes can be accessed through a DBSession instance
    Base.metadata.bind = engine
    # DB session to connect to DB and keep any changes in a "staging zone"
    DBSession = sessionmaker(bind=engine)

    # iterate through the dataframe rows
    for index, row in kin_sub_dataframe.iterrows():
        # open a SQLite session
        session = DBSession()
        # TODO get the primary keys in the row
        # get the kinase accession number in the df row
        new_kin_acc = row['KIN_ACC_ID']
        # print('new_kin_acc', new_kin_acc)
        # check if accession already in kinases table
        query_res = session.query(Kinase) \
            .filter(Kinase.kin_accession == new_kin_acc).first()
        # print('query_res', query_res)
        # kinase accession number not in table
        if query_res is None:
            kinase = Kinase(kin_accession=new_kin_acc)
        else:
            kinase = query_res
        for df_heading, class_match in kin_sub_human_to_class.items():
            class_name = class_match[0]
            class_attr = class_match[1]
            if class_name == Kinase and class_attr != 'kin_accession':
                attr = getattr(kinase, class_attr, None)
                if (attr in [None, '', ' ', 'nan', 'NaN']):
                    setattr(kinase, class_attr, row[df_heading])
        session.add(kinase)
        session.commit()
        session.close()

# class.attr.primary_key boolean
import_kinase_substrate_data(kin_sub_human)
#
#
#
#             'SUB_ACC_ID'
#
#
#
# # import relevant fields from kin_sub df into corresponding classes.attributes
# # check if primary keys are already in table
# # if in table, check info matches
# # try adding except if primary key error?
#
#
# for index, row in kin_sub_human.iterrows():
#     session = DBSession()
#     # get the kinase accession number in the df row
#     new_kin_acc = row['KIN_ACC_ID']
#     # check if accession already in kinases table
#     query_res = session.query(Kinase.kin_accession)\
#         .filter(Kinase.kin_accession == new_kin_acc).first()
#     if query_res is not None:
#         if query_res.
#
#
# for row in df:
#     session = DBSession()
#
#     sqlalchemy query
#     Kinase(kin_acc_num=df['KIN_ACC_ID'])
#     session.commit()
#     session.close()
#
#
# session.add_all([
#     Kinase(kin_acc_num='AA00001', kin_name='Kinase 1', kin_gene='KIN1',
#            kin_prot='Kin1', kin_org='H. sapiens', kin_loc='cytoplasm',
#            kin_fam='family 1'),
#     Kinase(kin_acc_num='AA00002', kin_name='Kinase 2', kin_gene='KIN2',
#            kin_prot='Kin2', kin_org='H. sapiens', kin_loc='nucleous',
#            kin_fam='family 1'),
#     Kinase(kin_acc_num='AA00003', kin_name='Kinase 3', kin_gene='KIN3',
#            kin_prot='Kin3', kin_org='H. sapiens', kin_loc='nucleous',
#            kin_fam='family 2'),
#     Kinase(kin_acc_num='AA00004', kin_name='Kinase 4', kin_gene='KIN4',
#            kin_prot='Kin4', kin_org='H. sapiens', kin_loc='cytoplasm',
#            kin_fam='family 3'),
#     Kinase(kin_acc_num='AA00005', kin_name='Kinase 5', kin_gene='KIN5',
#            kin_prot='Kin5', kin_org='H. sapiens', kin_loc='cytoplasm',
#            kin_fam='family 3'),
#     Substrate(subs_acc_num='SU00001', subs_name='Substrate 1',
#               subs_gene_id='S001', subs_gene='SUB1', subs_org='H. sapiens',
#               subs_mod_res='T', subs_domain='domain 1', subs_ab='XX-0001'),
#     Substrate(subs_acc_num='SU00002', subs_name='Substrate 2',
#               subs_gene_id='S002', subs_gene='SUB2', subs_org='H. sapiens',
#               subs_mod_res='S', subs_domain='domain 1', subs_ab='XX-0002'),
#     Substrate(subs_acc_num='SU00003', subs_name='Substrate 3',
#               subs_gene_id='S003', subs_gene='SUB3', subs_org='H. sapiens',
#               subs_mod_res='T', subs_domain='domain 2', subs_ab='XX-0003'),
#     Substrate(subs_acc_num='SU00004', subs_name='Substrate 4',
#               subs_gene_id='S004', subs_gene='SUB4', subs_org='H. sapiens',
#               subs_mod_res='S', subs_domain='domain 1', subs_ab='XX-0004'),
#     Substrate(subs_acc_num='SU00005', subs_name='Substrate 5',
#               subs_gene_id='S005', subs_gene='SUB5', subs_org='H. sapiens',
#               subs_mod_res='T', subs_domain='domain 2', subs_ab='XX-0005')])
#
#
# # commit all changes
# session.commit()