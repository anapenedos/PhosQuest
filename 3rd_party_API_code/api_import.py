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


    ### Generic version
    # x = urllib.request.urlopen('https://www.google.co.uk')
    # print(x.read())

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

    ### The two lines of code below are to overcome some websites that do not want programs or python (i.e. not real users) to come and take data from their website (they basically only want real users). Thus you will usually get blocked. A way around this is to denote a User-Agent which is basically telling the website being searched that we are a human.

    # This code sets the "contact" variable which is used in the next code
    contact = ""  # Please set a contact email address here to help us debug in case of problems (see https://www.uniprot.org/help/privacy). I am not sure you need an email as it worked for both with and withouut"

    # This code tells the API we are a human (I am not sure this is needed, as it worked without)
    request.add_header('User-Agent', 'Python %s' % contact)

    # This code opens the URL with paramters
    response = urllib.request.urlopen(request)

    # This code reads the details with a limit defined (not sure if this is bytes???)
    # page = response.read(200000)

    # Print the data (we can also output this as a text file)
    # print(page)

    df = pd.read_table(response)
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