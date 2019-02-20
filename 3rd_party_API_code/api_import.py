import pandas as pd

### Import modules
import urllib.request
import urllib.parse


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


    # The default base URL
    url = 'https://www.uniprot.org/uploadlists/'

    # Example parameters
    params = {
        'from': 'ACC',
        'to': 'ACC',
        'format': 'tab',
        'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families',
        'query': api_query_accessions
    }

    # This code takes the parameters and encodes it as it should be in the URL (e.g. %20 = 'a space')
    data = urllib.parse.urlencode(params)

    # This code changes it to a type of encoding, e.g. bytes
    data = data.encode('utf-8')

    # This code requests the URL and and data (which has already been encoded above)
    request = urllib.request.Request(url, data)

    # This code opens the URL with paramters
    response = urllib.request.urlopen(request)

    df = pd.read_table(response)

    df['Subcellular location55'] = df['Subcellular location [CC]'].astype(str)
    df['Subcellular location55'] = df['Subcellular location55'].str.extract('(?<=SUBCELLULAR LOCATION: )(.*?)(?={)', expand=True)

    # df.to_csv('output4.csv')

    return df # columns: Accession, location, family, full protein name

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
