### UniProt API for a single accession number

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd

# --------------------------------------------------------------------------- #

### API code for a single accession number

### Select the specific accession number to search from 
url = 'https://www.uniprot.org/uniprot/?query=Q64303'

### The url is read into a dataframe
dfs = pd.read_html(url)

### Print the results. Here we can select specific data frames which relate to tables from the website. 
print(dfs[0:3])
