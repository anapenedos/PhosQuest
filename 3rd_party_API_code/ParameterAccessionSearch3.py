### The following code has the following features:-
### Uses the UniProt webservice
### Prints to output3 file, tabulated
### Only works with one Accession number


#pip install bioservices
#pip install seaborn


import io
import pandas as pd

import urllib.request
import urllib.parse

#Import bioservices module, to run remote UniProt queries
from bioservices import UniProt

#Make a link to the UniProt webservice
service = UniProt()

# Build a query string
query = "accession:G1FDY4"

# Define a list of colums we want to retrieve
columnlist = "id,feature(SUBCELLULAR LOCATION),feature(INTRAMEMBRANE),feature(TOPOLOGICAL DOMAIN),feature(TRANSMEMBRANE),domains,domain,comment(DOMAIN)"

# Send the query to UniProt, and catch the search result in a variable
result = service.search(query, frmt="tab", columns=columnlist)

#df = pd.read_table(io.StringIO(result), header=None)
#df

df = pd.read_table(io.StringIO(result))
df.to_csv('output3.csv')

# Inspect the result
#print(result)

