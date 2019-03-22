### API import script from PubChem.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd

# --------------------------------------------------------------------------- #

### PubChem API data access form PubChem website.

### URL saved to a .csv with specific accession numbers.
url_csv = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/224,624113/property/IUPACName,MolecularFormula,MolecularWeight/csv'

# Converted to a dataframe.
df = pd.read_csv(url_csv)

# Output as a csv.
df.to_csv('PubChem_output.csv')





