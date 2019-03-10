import pandas as pd
import numpy as np
from itertools import chain


def reset_df_index(data_frame):
    """
    Resets pandas data frame index, dropping current index and replacing it
    with a "clean" index in place. Useful after data frame filtering and multi-
    value column splitting.

    :param data_frame: pandas data frame (pd df)
    :return: resets index index in place in original df (None)
    """
    return data_frame.reset_index(drop=True, inplace=True)


def get_column_with_single_values(data_frame_column, multi_value_separator):
    """
    From a data frame series object returns a list of values in the same
    order as the data frame column where all values in each row have been split
    at the separator given.
    e.g., 3, 4, 5    >   [3, 4, 5, 'c', 'f']
          c,   f

    :param data_frame_column: data frame column (pd series)
    :param multi_value_separator: multi-values separator (str)
    :return: list of single values (list of str)
    """
    # split values at separator
    split_lines_list = list(chain.from_iterable(
        data_frame_column.str.split(multi_value_separator)))
    # remove any leading and trailing spaces
    stripped_list = list(map(str.strip, split_lines_list))
    return stripped_list


def split_multi_value_rows_in_df(data_frame, column_heading, separator):
    """
    Takes in a data frame and a column headings and returns a new data frame
    where the rows containing multiple values in the columns with headings
    given are split into different rows, repeating the remaining fields in the
    data frame.
    e.g.,    A       B       C                A       B       C
           _____   _____   _____     >      _____   _____   _____
             1       2    3, 4, 5             1       2       3
             a       b    c,   f              1       2       4
                                              1       2       5
                                              a       b       c
                                              a       b       f

    :param data_frame: pandas data frame object (df)
    :param column_heading: name of column heading (str)
    :param separator: multi-values separator (str)
    :return: data frame with relevant column containing multiple values split
             in multiple rows (df)
    """
    # calculate number of values per row in the multi-value column
    lens = data_frame[column_heading].str.split(separator).map(len)

    # define a dictionary mapping a column heading to the re-arranged data
    new_data = {}
    for col in data_frame.columns:
        # if the column is not the one with multiple values, repeat values the
        # same number of times as there are multiple values in the column to
        # split
        if col not in [column_heading, None]:
            new_data[col] = np.repeat(data_frame[col], lens)
        # if the column is the one with multiple values, produce a new column
        # where multi-value lines are split to multiple lines
        elif col == column_heading:
            new_data[col] = get_column_with_single_values(data_frame[col],
                                                          separator)
    single_val_df = pd.DataFrame(new_data)
    # resets index so no index warnings follow data frame
    reset_df_index(single_val_df)
    return single_val_df


def create_db_kin_links(accessions_set):
    """
    From a set of kinase accessions, produce url links to detail page of each
    kinase. If 'not in DB', 'not in DB' is returned

    :param accessions_set: set of kinase accessions (set of str)
    :return: string containing links to each kinase (str)
    """
    if accessions_set != 'not in DB':
        link_collection = ''
        for acc in sorted(accessions_set):
            link_collection += "<a href='/kin_detail/%s'>%s</a> " % (acc, acc)
    else:
        link_collection = 'not in DB'
    return link_collection


'http://127.0.0.1:5000/sub_detail/Q9UQL6'