### Import relevant modules
import pandas as pd

### Select the specific accession number to search from 
url = 'https://www.uniprot.org/uniprot/?query=Q64303'

### Define a variable, here denoted as dfs (dataframes)
dfs = pd.read_html(url)

### Print the results. Here we can select specific data frames which relate to tables from the website. 
print(dfs[0:3])
