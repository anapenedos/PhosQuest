### Python script to search and save as csv the search results form PubChem.

### Import relevant modules
import pandas as pd
import urllib

from .api_import import get_kinase_info

# import required data frames
kinase_accession_list = get_kinase_info()

args = {kinase_accession_list}
url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/property/IUPACName/csv".format(urllib.urlencode(args))

### Select the specific accession number to search from
url_csv = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/property/IUPACName/csv'

df = pd.read_csv(url_csv)
#df.to_csv('output5.csv')