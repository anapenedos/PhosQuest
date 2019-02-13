# Standard library imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

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

    # get classes in data frame
    classes_in_df = set()
    for df_heading, class_match in kin_sub_human_to_class.items():
        class_name = class_match[0]
        classes_in_df.add(class_name)

    # get classes primary keys attributes
    classes_keys = {}  # {Kinase: ['kin_accession'], ...}
    for available_class in classes_in_df:
        classes_keys[available_class] = \
            inspect(available_class).primary_key[0].name

    # iterate through the dataframe rows
    for index, row in kin_sub_dataframe.iterrows():
        # open a SQLite session
        session = DBSession()

        # get keys for classes in row
        # dictionary of primary key values to class and key they belong to
        new_key_to_table = {}  # {key_value: (class, attr), ...}
        for df_heading, class_match in kin_sub_human_to_class.items():
            # df heading corresponds to class and class attribute
            class_name = class_match[0]
            class_attr = class_match[1]
            # if the df heading contains a primary, add key to the dict
            if class_attr in classes_keys.values():
                new_key_to_table[row[df_heading]] = (class_name, class_attr)

        # check if records already exist in tables and obtain class instances
        class_instances = {}  # {Class: class_instance, ...}
        for obj_key, class_info in new_key_to_table.items():
            class_name = class_info[0]
            class_attr = class_info[1]
            query_res = session.query(class_name)\
                .filter(getattr(class_name, class_attr) == obj_key).first()
            # create new class instance if not
            if query_res is None:
                class_instance = class_name(**{class_attr: obj_key})
                session.add(class_instance)
            # get the existing class instance if so
            else:
                class_instance = query_res
            # keep track of the new instances
            class_instances[class_name] = class_instance

        # get remaining attributes for each instance
        for instance_class_name, class_instance in class_instances.items():
            for df_heading, class_match in kin_sub_human_to_class.items():
                class_name = class_match[0]
                class_attr = class_match[1]
                if class_name == instance_class_name:
                    attr = getattr(class_instance, class_attr, None)
                    if (attr in [None, '', ' ', 'nan', 'NaN']):
                        setattr(class_instance, class_attr, row[df_heading])
            session.add(class_instance)
            session.commit()

        # TODO set up related objects


        session.close()


# class.attr.primary_key boolean
import_kinase_substrate_data(kin_sub_human)
