### API import script from PubChem.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd

# --------------------------------------------------------------------------- #

### PubChem API data access form PubChem website.

### URL saved to a .csv with specific accession numbers.
#url_csv = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science[journal]+AND+breast+cancer+AND+2018[pdat]'
url_csv = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id=Q86UU0&rettype=&retmode=text'

#print(url_csv)

# Converted to a dataframe.
df = pd.read_table(url_csv)
row_data = df.loc[3:3]
print(row_data)
#test
# Output as a csv.
#df.to_csv('PubChem_output.csv')





