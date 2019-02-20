### The following code has the following features:-
### Uses the uniprot.org/uploadlists website
### Prints to output4 file, tabulated
### Works with multiple Accession number

import io
import pandas as pd
import re

### Import modules
import urllib.request
import urllib.parse

# The default base URL
url = 'https://www.uniprot.org/uploadlists/'

# Example parameters
params = {
        'from':'ACC',
        'to':'ACC',
        'format':'tab',
        'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families',
        'query':'G1FDY4 P13368 Q9BQI6'
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

df.to_csv('output4.csv')

