import sys
from sqlalchemy.inspection import inspect


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


# def str_to_class(classname):
#     return reduce(getattr, str.split("."), sys.modules[__name__])
