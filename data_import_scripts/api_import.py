# Functions for import of API data

# standard library imports
from sqlalchemy.inspection import inspect
import pandas as pd
import urllib.request
import urllib.parse
import urllib
import time

# project-specific imports
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.class_functions import get_class_key_attrs

# =========================================================================== #


def get_table_values_for_search(class_name):
    """
    Produces a list of the key values in class_name table that will be used in
    the API search. Works for classes with single primary key only.

    :param class_name: a sqlalchemy declarative class (sqlalchemy class object)
    :return: list of key values for search (list)
    """
    print('Obtaining key values for %s records in DB' % class_name.__name__)
    # get the name of the primary key attribute in the class's corresponding
    # table
    key_attr = get_class_key_attrs(class_name, single_key=True)

    # create a DB session
    session = create_sqlsession()
    # list of the value for the key field for all records [('val1',),...]
    records = session.query(getattr(class_name, key_attr)).all()
    # close the session
    session.close()

    # convert into list of str ['val1', ...]
    keys_list = [val[0] for val in records]

    print('Retrieved key values for %i %s records'
          % (len(keys_list), class_name.__name__))

    return keys_list


def get_uniprot_api_data(class_name):
    """
    Obtains UniProt data for the objects currently in the DB table
    corresponding to class_name and returns a data frame where required
    information has been parsed.

    :param class_name: a sqlalchemy declarative class (sqlalchemy class object)
    :return: pandas data frame (df)
    """
    print('Retrieving UniProt data for %s records' % class_name.__name__)

    # Get all class_name table key values
    keys_list = get_table_values_for_search(class_name)
    # convert list into Uniprot query format 'val1 val2'
    query_str = ' '.join(keys_list)

    # Get the corresponding data
    # The default base URL.
    url = 'https://www.uniprot.org/uploadlists/'

    # Parameters for UniProt API site, selecting specific qualifiers using the
    # api_query_accession variable from the accession list function.
    params = {
        'from': 'ACC',
        'to': 'ACC',
        'format': 'tab',
        'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families,'
                   'genes,proteome,comment(DOMAIN)',
        'query': query_str
    }

    # Takes the parameters and encodes it as it should be in the URL
    # (e.g. %20 = 'a space').
    data = urllib.parse.urlencode(params)

    # Changes it to a type of encoding, e.g. bytes.
    data = data.encode('utf-8')

    # Requests the URL and and data (which has already been encoded above).
    request = urllib.request.Request(url, data)

    # Opens the URL with paramters.
    response = urllib.request.urlopen(request)

    # Places the data into a dataframe.
    df = pd.read_table(response)

    # Converts a replicate Subcellular location column in string format.
    df['Subcellular location55'] = df['Subcellular location [CC]'].astype(str)

    # Specfiically extracts the Subcellular location information (and nothing
    # else) from the original column and places is /
    # within the new Subcellular loation columns.
    df['Subcellular location55'] = df['Subcellular location55'].str.extract(
        '(?<=SUBCELLULAR LOCATION: )(.*?)(?={)', expand=True)

    # extract single protein name
    df['Protein name'] = df['Protein names'].astype(str)
    df['Protein name'] = df['Protein name'].str.extract(
        '^([^(]*?)(?: *\(.*)?$', expand=False)

    print('UniProt data obtained for %i %s records'
          % (len(keys_list), class_name.__name__))

    return df


def get_pubchem_api_data(class_name):
    """
    Obtains PubChem data for the objects currently in the DB table
    corresponding to class_name and returns a data frame where required
    information has been parsed.

    :param class_name: a sqlalchemy declarative class (sqlalchemy class object)
    :return: pandas data frame (df)
    """
    print('Retrieving PubChem data for %s records' % class_name.__name__)

    # Get all class_name table key values
    keys_list = get_table_values_for_search(class_name)

    # iterate through slices of the list to prevent exceeding of PubChem
    # programmatic data gathering request length limit
    dfs = []
    i = 0
    j = 50
    num_params = len(keys_list)
    while i < num_params:
        if j <= num_params:
            slice_end = j
        else:
            slice_end = num_params

        list_slice = keys_list[i: slice_end]

        # convert list into PubChem query format 'val1,val2'
        query_str = ','.join(str(i) for i in list_slice)

        results_csv = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
                       "cid/" + query_str + "/property/IUPACName,"
                       "MolecularFormula,MolecularWeight/csv")
        # Convert the csv to a data frame and append to the list
        dfs.append(pd.read_csv(results_csv))
        # update slice ends
        i += 50
        j += 50
        # introduce waiting time to prevent exceeding of PubChem
        # programmatic data gathering request# 5/s limit
        time.sleep(.2)

    # concatenate data frames resulting from all slices into a single data
    # frame
    full_df = pd.concat(dfs)

    print('PubChem data obtained for %i %s records'
          % (len(keys_list), class_name.__name__))

    return full_df