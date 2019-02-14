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
    classes_keys = {}  # {Class: ['key_attr_1', 'key_attr_2'], ...}
    for class_in_df in classes_in_df:
        # produce list of primary keys for each class_in_df for all the classes
        # present in the data frame (from the classes_in_df set)
        keys_of_class = [key.name for key in inspect(class_in_df).primary_key]
        # add a dictionary entry from the class_in_df to corresponding list of
        # primary keys
        classes_keys[class_in_df] = keys_of_class

    # iterate through the data frame rows (of the data frame containing data to
    # import) to:
    # 1. set up new instances of classes or retrieve existing instances
    # from the db
    # 2. populate instance class attributes from data frame data
    # 3. generate relationships between instances of different classes
    for index, row in kin_sub_dataframe.iterrows():
        # open a SQLite session
        session = DBSession()

        # get keys for classes in row
        # dictionary of class to primary key attributes and key values tuples
        new_table_keys = {}  # {class: {key_attr: key_value, ...}, ...}
        # iterate through dict mapping df_heading: (Class, class_attr)
        for df_heading, class_match in kin_sub_human_to_class.items():
            # df heading corresponds to class and class attribute
            class_name = class_match[0]
            class_attr = class_match[1]
            # if the df heading contains a primary key, add key value to dict
            if class_attr in classes_keys[class_name]:
                # append the new (key_attr, key_value) tuple to the
                # new_table_keys dict entry for the class if class in dict
                if class_name in new_table_keys:
                    new_table_keys[class_name][class_attr] = row[df_heading]
                # add class and its first value to new_table_keys dict if
                # class not in dict
                else:
                    new_table_keys[class_name] = {class_attr: row[df_heading]}  # look setdefault

        # check if records already exist in tables and obtain class instances
        class_instances = {}  # {Class: class_instance, ...}
        for class_name, keys_info in new_table_keys.items():  # {class: {key_attr: key_value, ...}, ...}
            # create query object
            query_res = session.query(class_name)
            # apply filters to the query_res based on primary keys
            for key_attr, key_value in keys_info.items():
                query_res = query_res.filter(
                    getattr(class_name, key_attr) == key_value)
            # given query_res was filterd by all primary keys in table, it
            # should now list a single instance, which can be obtained with
            # .first
            query_res = query_res.first()
            # create new class instance if not
            if query_res is None:
                class_instance = class_name(**keys_info)
                session.add(class_instance)
            # get the existing class instance if so
            else:
                class_instance = query_res
            # keep track of the new instances
            class_instances[class_name] = class_instance

        # get remaining attributes for each instance
        for instance_class_name, class_instance in class_instances.items():
            # get the class attributes
            for df_heading, class_match in kin_sub_human_to_class.items():
                class_name = class_match[0]
                class_attr = class_match[1]
                if class_name == instance_class_name:
                    attr = getattr(class_instance, class_attr, None)
                    if (attr in [None, '', ' ', 'nan', 'NaN']):
                        setattr(class_instance, class_attr, row[df_heading])
            # session.add(class_instance)
            # session.commit()

        # add relationship field
        kinase_in_row = class_instances[Kinase]
        phosphosite_in_row = class_instances[Phosphosite]
        substrate_in_row = class_instances[Substrate]
        # kinase phosphorylates relationship
        kinase_in_row.kin_phosphorylates.append(phosphosite_in_row)
        # substrate field in phosphosite table
        phosphosite_in_row.phos_in_substrate = substrate_in_row.subs_accession
        # phosphosite belongs to substrate relationship
        phosphosite_in_row.site_in_subs = substrate_in_row
        # TODO set up related objects
        # session.add(kinase_in_row)
        # session.add(phosphosite_in_row)
        # session.add(substrate_in_row)
        session.commit()
        session.close()


import_kinase_substrate_data(kin_sub_human)

# pd DF.to_sql
# if needed,
# class.attr.primary_key boolean
# If the model class is User and there are many primary keys,
# >>> from sqlalchemy.inspection import inspect
# >>> [key.name for key in inspect(User).primary_key]
# ['id', 'name']

##############################
### SQLite useful commands ###
##############################

#  to get into database
# from giardello folder in terminal
# `sqlite3 database/PhosphoQuest.db`

# to show table headers
# `sqlite>.header on`

# to how entries in columns
# `sqlite>.mode column`

# to show all entries in a TABLE
# `SELECT * FROM TABLE;`

# to sort results by COLUMN
# `SELECT * FROM TABLE ORDER BY COLUMN;`

# to count all entries in a TABLE
# `SELECT COUNT(*) FROM TABLE;`


