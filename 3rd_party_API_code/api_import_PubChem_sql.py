### API import script from PubChem which then adds data to the SQLite database.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
import urllib

# --------------------------------------------------------------------------- #

### Import the Function from api_import.py allowing accession number list to be obtained from sql database.
from .api_import import get_kinase_info

# --------------------------------------------------------------------------- #

### PubChem API data access form PubChem website.

# import required data frames
kinase_accession_list = get_kinase_info()

# Incorporate the list of kinase variable into the url.
args = {kinase_accession_list}
url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/property/IUPACName/csv".format(urllib.urlencode(args))

### Save the url as a csv.
url_csv = 'url'

# Convert the csv to a dataframe.
df = pd.read_csv(url_csv)

#df.to_csv('output5.csv')