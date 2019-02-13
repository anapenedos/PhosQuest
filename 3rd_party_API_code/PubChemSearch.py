### Python script to search and save as csv the search results form PubChem.

### Import relevant modules
import pandas as pd

### Select the specific accession number to search from
url_csv = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/224,624113/property/IUPACName/csv'

df = pd.read_csv(url_csv)
df.to_csv('output5.csv')





