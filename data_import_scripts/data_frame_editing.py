import pandas as pd
import numpy as np
from itertools import chain


def get_column_with_single_values(data_frame_column, multi_value_separator):
    """
    From a data frame series object returns a list of values in the same
    order as the data frame column where all values in each row have been split
    at the separator given.
    e.g., 3, 4, 5    >   [3, 4, 5, 'c', 'f']
          c,   f
    :param data_frame_column: data frame column (df series)
    :param multi_value_separator: multi-values separator (str)
    :return: list of single values (list of str)
    """
    return list(chain.from_iterable(
        data_frame_column.str.split(multi_value_separator)))


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

    # define a dictionary mapping a column to how its entries are treated
    new_data = {}
    for col in data_frame.columns:
        if col not in [column_heading, None]:
            new_data[col] = np.repeat(data_frame[col], lens)
        elif col == column_heading:
            new_data[col] = get_column_with_single_values(data_frame[col],
                                                          separator)
    single_val_df = pd.DataFrame(new_data)
    return single_val_df


# # testing
# df=pd.DataFrame(data=[['1','2','3,4,5'], ['a', 'b', 'c,   d']],
#                 columns=['A','B','C'])
# print(df, '\n')
# sdf = split_multi_value_rows_in_df(df, 'C', ',')
# print(sdf)
