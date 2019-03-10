# Standard library imports
from sqlalchemy.inspection import inspect
from datetime import datetime, timedelta
from pandas import isnull

# project imports
from PhosphoQuest_app.data_access.db_sessions import import_session_maker
from PhosphoQuest_app.data_access.class_functions import get_classes_key_attrs

# define null-type of values that are treated differently
NULL_VALS = [None, '', ' ', '-', 'nan', 'NaN']


def get_key_vals(df_to_class_dict, classes_keys, row):
    """
    Gets the key values for the class instances in a data frame row.

    :param df_to_class_dict: data frame heading to class & attribute (dict)
                             {'DF header': [(Class, 'class_attribute')]}
    :param classes_keys: {Class: ['key_attr1', ...], ...} (dict)
    :param row: pandas data frame row (df row)
    :return: key values for the class instances in the row (dict)
             {class: {key_attr: key_value, ...}, ...}
    """
    # get keys for classes in row
    # dictionary of class to primary key attributes and key values tuples
    new_table_keys = {}  # {class: {key_attr: key_value, ...}, ...}
    # iterate through dict mapping df_heading: (Class, class_attr)
    for df_heading, class_matches in df_to_class_dict.items():
        for class_match in class_matches:
            # df heading corresponds to class and class attribute
            class_name = class_match[0]
            class_attr = class_match[1]
            # if the row contains a non-null value and the df heading
            # contains a primary key, add key value to dict
            if (class_attr in classes_keys[class_name]
                and row[df_heading] not in NULL_VALS
                and not isnull(row[df_heading])):
                new_values = new_table_keys.setdefault(class_name, {})
                new_values[class_attr] = row[df_heading]
    return new_table_keys


def get_instances(new_table_keys, session):
    """
    Check if records already exist in tables and obtain class instances. Create
    new instances if not in tables.

    :param new_table_keys: key values for the class instances in the row (dict)
                           {class: {key_attr: key_value, ...}, ...}
    :param session: a sqlalchemy DB session (sqlalchemy session)
    :return: dictionary of instance for each class (dict)
             {Class: class_instance, ...}
    """
    # check if records already exist in tables and obtain class instances
    class_instances = {}  # {Class: class_instance, ...}
    for class_name, keys_info in new_table_keys.items():
        # create query object
        query_res = session.query(class_name)
        # apply filters to the query_res based on primary keys
        for key_attr, key_value in keys_info.items():
            query_res = query_res.filter(
                getattr(class_name, key_attr) == key_value)
        # given query_res was filtered on all primary keys in table, it
        # should now list a single instance, which can be obtained with
        # .first
        query_res = query_res.first()
        # create new class instance if no record retrieved by query
        # and none of the key values is None
        if query_res is None:
            class_instance = class_name(**keys_info)
            session.add(class_instance)
        # or get the existing class instance if already in table
        else:
            class_instance = query_res
        # keep track of the new instances
        class_instances[class_name] = class_instance
    return class_instances


def import_attrs(class_instances, df_to_class_dict, row):
    """
    Get instance attributes for each instance from a pandas data frame row.

    :param class_instances: dictionary of instance for each class (dict)
                            {Class: class_instance, ...}
    :param df_to_class_dict: data frame heading to class & attribute (dict)
                             {'DF header': [(Class, 'class_attribute')]}
    :param row: pandas data frame row (df row)
    :return: updates class_instances dict (None)
    """
    # get remaining attributes for each instance
    for instance_class_name, class_instance in class_instances.items():
        # get the class attributes
        for df_heading, class_matches in df_to_class_dict.items():
            for class_match in class_matches:
                class_name = class_match[0]
                class_attr = class_match[1]
                if class_name == instance_class_name:
                    attr = getattr(class_instance, class_attr, None)
                    # if the existing instance attr is not defined, set it
                    # to the value in the data frame
                    if attr in NULL_VALS:
                        setattr(class_instance, class_attr, row[df_heading])
    return


def import_data_from_data_frame(df, df_to_class_dict):
    """
    Takes in data frame storing kinase substrate info and populates relevant
    entries in SQLite database.

    :param df: pandas data frame from PhosphositePlus import (df)
    :param df_to_class_dict: data frame heading to class & attribute (dict)
                             {'DF header': [(Class, 'class_attribute')]}
    """
    start_time = datetime.now()
    print('Started processing data frame\n%s\n'
          'Current time: %s)'
          % (df.head(3), start_time.strftime("%d-%m-%Y %H:%M:%S")))
    # get classes in data frame from dict function argument
    classes_in_df = set()
    for df_heading, class_matches in df_to_class_dict.items():
        for class_match in class_matches:
            class_name = class_match[0]
            classes_in_df.add(class_name)

    # get classes primary keys attributes
    # Class: ['key_attr1', ...]
    classes_keys = get_classes_key_attrs(classes_in_df)

    # set up a row counter
    processed_rows = 0
    total_records = len(df)

    # Create session maker
    DBSession = import_session_maker()

    # iterate through the data frame rows (of the data frame containing data to
    # import) to:
    # 1. set up new instances of classes or retrieve existing instances
    # from the db
    # 2. populate instance class attributes from data frame data
    # 3. generate relationships between instances of different classes
    for index, row in df.iterrows():
        # Issue print statement every 1000 records
        if processed_rows % 1000 == 0:
            print('Processing row %i of %i rows in data frame'
                  % (processed_rows, total_records))
        # open a SQLite session
        session = DBSession()

        # get keys for classes in row
        # dictionary of class to primary key attributes and key values tuples
        # {class: {key_attr: key_value, ...}, ...}
        new_table_keys = get_key_vals(df_to_class_dict, classes_keys, row)

        # check if records already exist in tables and obtain class instances
        # {Class: class_instance, ...}
        class_instances = get_instances(new_table_keys, session)

        # get remaining attributes for each instance
        import_attrs(class_instances, df_to_class_dict, row)

        # if more than one class in the data frame, set up relationships
        if len(classes_in_df) > 1:
            for class_instance in class_instances.values():
                class_instance.add_relationships(class_instances)
        # commit the new/updated objects to the DB
        session.commit()
        session.close()

        # update row counter
        processed_rows += 1
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('Completed processing %i records in data frame\n%s\n'
          'Current time: %s\n'
          'Time elapsed: %s\n'
          % (total_records, df.head(3),
             end_time.strftime("%d-%m-%Y %H:%M:%S"),
             timedelta(days=elapsed_time.days, seconds=elapsed_time.seconds)))
