import sys
from sqlalchemy.inspection import inspect
import PhosphoQuest_app.data_access.sqlalchemy_declarative


def str_to_class(class_str):
    """
    Given a string matching the name of a class in the sqlalchemy declarative
    script, returns the class object matching the string.
    """
    return getattr(PhosphoQuest_app.data_access.sqlalchemy_declarative,
                   class_str)


def get_class_key_attrs(class_name, single_key=False):
    """
    Given a sqlalchemy Class, returns list of primary key attributes for the
    class or single primary key attribute if single_key=True.

    :param class_name: sqlalchemy Class (class obj)
    :param single_key: single key is expected (True) or multiple keys (False)
                       (boolean)
    :return: list of class attributes that are primary keys (list of str)
             primary key attribute if single_key=True (str)
    """
    keys_of_class =  [key.name for key in inspect(class_name).primary_key]
    if single_key:
        key_str = keys_of_class[0]
        keys_to_return = key_str
    else:
        keys_to_return = keys_of_class
    return keys_to_return


def get_classes_key_attrs(classes_iterable, single_key=False):
    """
    Given an iterable object of sqlalchemy classes returns a dictionary where
    each class is mapped to a collection of primary key attributes or a single
    key attribute if single_key=True.

    :param classes_iterable: iterable containing sqlalchemy classes (iter)
    :param single_key: single key is expected (True) or multiple keys (False)
                       (boolean)
    :return: dictionary Class: ['key_attr1', ...] when single_key=False or
                        Class: 'key_attr' single_key=True (dict)
    """
    class_keys = {}
    # obtain key attributes for each class
    for class_name in classes_iterable:
        class_keys[class_name] = get_class_key_attrs(class_name, single_key)

    return class_keys
