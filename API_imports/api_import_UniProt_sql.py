### API import script from UniProt which then adds data to the SQLite database.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
import urllib.request
import urllib.parse

# --------------------------------------------------------------------------- #

### Function to read accession number list from sql database.
def get_kinase_info(accession_number_list):
    """
    takes in an accession number and returns
    :param accession_number_list: a list of all accessions in kinase table
                ['AA0001', 'BB33440', ....]
    :return: dataframe with necessary info (dataframe)
    """

    # convert list to API query format
    api_query_accessions = accession_number_list[0]
    for accession in accession_number_list[1:]:
        api_query_accessions = api_query_accessions + ' ' + accession

# --------------------------------------------------------------------------- #

### UniProt API data access form uniprot website.

    # The default base URL
    url = 'https://www.uniprot.org/uploadlists/'

    # Parameters for UniProt API site, selecting specific qualifiers using the api_query_accession variable from the accession list function.
    params = {
        'from': 'ACC',
        'to': 'ACC',
        'format': 'tab',
        'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families',
        'query': api_query_accessions
    }

    # Takes the parameters and encodes it as it should be in the URL (e.g. %20 = 'a space').
    data = urllib.parse.urlencode(params)

    # Changes it to a type of encoding, e.g. bytes
    data = data.encode('utf-8')

    # Requests the URL and and data (which has already been encoded above).
    request = urllib.request.Request(url, data)

    # Opens the URL with paramters.
    response = urllib.request.urlopen(request)

    # Places the data into a dataframe.
    df = pd.read_table(response)

    # Converts a replicate Subcellular location column in string format.
    df['Subcellular location55'] = df['Subcellular location [CC]'].astype(str)

    # Specfiically extracts the Subcellular location information (and nothing else) from the orignal column and places is /
    # within the new Subcellular loation columns.
    df['Subcellular location55'] = df['Subcellular location55'].str.extract('(?<=SUBCELLULAR LOCATION: )(.*?)(?={)', expand=True)

    # df.to_csv('output4.csv')
    return df # columns: Accession, location, family, full protein name.

# --------------------------------------------------------------------------- #

"""
option A
########
query our DB
get all accession numbers of kinases in the DB
use the API script
get cellular location and family from uniprot as DF
input the cell location and fam into DB using an import script

option B
########
iterate through the kinases in the DB
for each one get the info required using the API
"""