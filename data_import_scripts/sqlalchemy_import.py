# Standard library imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

# Project imports
# classes and join tables
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate, \
    Phosphosite, Disease, DiseaseAlteration, Inhibitor, CellularLocation, \
    kinases_inhibitors_table, kinases_phosphosites_table
# data import data frames
from data_import_scripts.db_parsing import kin_sub_human, \
    phos_sites_human, reg_sites_human, dis_sites_human, mrc_inhib_source
# dataframe headings to class attribute dictionaries
from data_import_scripts.dataframes_to_attributes \
    import kin_sub_human_to_class, phos_sites_human_to_class, \
    reg_sites_human_to_class, dis_sites_human_to_class, \
    mrc_inhib_source_to_class


# TODO solve issue of multi tables to df heading in dict
# TODO correct dict format
def import_data_from_data_frame(df, df_to_class_dict):
    """
    Takes in data frame storing kinase substrate info and populates relevant
    entries in SQLite database.

    :param df: pandas data frame from PhosphositePlus import (df)
    :param df_to_class_dict: data frame heading to class & attribute (dict)
                             {'DF header': (Class, 'class_attribute')}
    """
    # Create engine that stores data to database\<file_name>.db
    db_path = os.path.join('database', 'PhosphoQuest.db')
    engine = create_engine('sqlite:///' + db_path)
    # Bind the engine to the metadata of the base class so that the
    # classes can be accessed through a DBSession instance
    Base.metadata.bind = engine
    # DB session to connect to DB and keep any changes in a "staging zone"
    DBSession = sessionmaker(bind=engine)

    # get classes in data frame
    classes_in_df = set()
    for df_heading, class_match in df_to_class_dict.items():
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
    for index, row in df.iterrows():
        # open a SQLite session
        session = DBSession()

        # get keys for classes in row
        # dictionary of class to primary key attributes and key values tuples
        new_table_keys = {}  # {class: {key_attr: key_value, ...}, ...}
        # iterate through dict mapping df_heading: (Class, class_attr)
        for df_heading, class_match in df_to_class_dict.items():
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
                    new_table_keys[class_name] = {class_attr: row[df_heading]}  # TODO look at setdefault

        # check if records already exist in tables and obtain class instances
        class_instances = {}  # {Class: class_instance, ...}
        for class_name, keys_info in new_table_keys.items():
            # create query object
            query_res = session.query(class_name)
            # apply filters to the query_res based on primary keys
            for key_attr, key_value in keys_info.items():
                query_res = query_res.filter(
                    getattr(class_name, key_attr) == key_value)
            # given query_res was filtered by all primary keys in table, it
            # should now list a single instance, which can be obtained with
            # .first
            query_res = query_res.first()
            # create new class instance if no record retrieved by query
            if query_res is None:
                class_instance = class_name(**keys_info)
                session.add(class_instance)
            # or get the existing class instance if already in table
            else:
                class_instance = query_res
            # keep track of the new instances
            class_instances[class_name] = class_instance

        # get remaining attributes for each instance
        for instance_class_name, class_instance in class_instances.items():
            # get the class attributes
            for df_heading, class_match in df_to_class_dict.items():
                class_name = class_match[0]
                class_attr = class_match[1]
                if class_name == instance_class_name:
                    attr = getattr(class_instance, class_attr, None)
                    if (attr in [None, '', ' ', 'nan', 'NaN']):
                        setattr(class_instance, class_attr, row[df_heading])

        # if more than one class in the data frame, set up relationships
        if len(classes_in_df) > 1:
            for class_instance in class_instances.values():
                class_instance.add_relationships(class_instances)
            #
            # # TODO make relationship set up universal
            # # add relationship fields
            # kinase_in_row = class_instances[Kinase]
            # phosphosite_in_row = class_instances[Phosphosite]
            # substrate_in_row = class_instances[Substrate]
            # # kinase phosphorylates relationship
            # kinase_in_row.kin_phosphorylates.append(phosphosite_in_row)
            # # substrate field in phosphosite table
            # phosphosite_in_row.phos_in_substrate = substrate_in_row.subs_accession
            # # phosphosite belongs to substrate relationship
            # phosphosite_in_row.site_in_subs = substrate_in_row
        session.commit()
        session.close()


# import_data_from_data_frame(kin_sub_human, kin_sub_human_to_class)
# import_data_from_data_frame(phos_sites_human, phos_sites_human_to_class)
# import_data_from_data_frame(reg_sites_human, reg_sites_human_to_class)
import_data_from_data_frame(dis_sites_human, dis_sites_human_to_class)
# import_data_from_data_frame(mrc_inhib_source, mrc_inhib_source_to_class)


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
# `.header on`

# to how entries in columns
# `.mode column`

# to show all entries in a TABLE
# `SELECT * FROM TABLE;`

# to sort results by COLUMN
# `SELECT * FROM TABLE ORDER BY COLUMN;`

# to count all entries in a TABLE
# `SELECT COUNT(*) FROM TABLE;`


