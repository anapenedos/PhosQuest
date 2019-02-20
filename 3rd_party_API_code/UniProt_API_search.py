### UniProt API import script with parsing.

### Uses the uniprot.org/uploadlists website/
### Prints to output file, tabulated/
### Works with multiple Accession number.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
import urllib.request
import urllib.parse

# --------------------------------------------------------------------------- #

### UniProt API data access form uniprot website.

# The default base URL.
url = 'https://www.uniprot.org/uploadlists/'

# Parameters for UniProt API site, selecting specific qualifiers using the api_query_accession variable from the accession list function.
params = {
        'from':'ACC',
        'to':'ACC',
        'format':'tab',
        'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families',
        'query':'G1FDY4 P13368 Q9BQI6'
        }

# Takes the parameters and encodes it as it should be in the URL (e.g. %20 = 'a space').
data = urllib.parse.urlencode(params)

# Changes it to a type of encoding, e.g. bytes.
data = data.encode('utf-8')

# Requests the URL and and data (which has already been encoded above).
request = urllib.request.Request(url, data)

# Opens the URL with paramters.
response = urllib.request.urlopen(request)

# Places the data into a dataframe.
df = pd.read_table(response)

# Converts a replicate Subcellular location column in string format.
df['Subcellular location55'] = df['Subcellular location [CC]'].astype(str)

# Specfiically extracts the Subcellular location information (and nothing else) from the orignal column and places is /
# within the new Subcellular loation columns.
df['Subcellular location55'] = df['Subcellular location55'].str.extract('(?<=SUBCELLULAR LOCATION: )(.*?)(?={)', expand=True)

# The datagframe is converted to a .csv file.
df.to_csv('UniProt_output.csv')

