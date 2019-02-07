### The following code has the following features:-
### Uses the uniprot.org/uploadlists website
### Prints to output4 file, tabulated
### Works with multiple Accession number

import io
import pandas as pd

### Import modules
import urllib.request
import urllib.parse

### Generic version
# x = urllib.request.urlopen('https://www.google.co.uk')
# print(x.read())

# The default base URL
url = 'https://www.uniprot.org/uploadlists/'

# Example parameters
params = {
        'from':'ACC',
        'to':'ACC',
        'format':'tab',
        'columns':'id,organism,database(PDB),comment(SUBCELLULAR LOCATION),feature(INTRAMEMBRANE),feature(TOPOLOGICAL DOMAIN),feature(TRANSMEMBRANE),comment(DOMAIN),families',
        'query':'G1FDY4 P13368 Q9BQI6'
        }

# This code takes the parameters and encodes it as it should be in the URL (e.g. %20 = 'a space')
data = urllib.parse.urlencode(params)

# This code changes it to a type of encoding, e.g. bytes
data = data.encode('utf-8')

# This code requests the URL and and data (which has already been encoded above)
request = urllib.request.Request(url, data)

### The two lines of code below are to overcome some websites that do not want programs or python (i.e. not real users) to come and take data from their website (they basically only want real users). Thus you will usually get blocked. A way around this is to denote a User-Agent which is basically telling the website being searched that we are a human.

# This code sets the "contact" variable which is used in the next code
contact = ""  # Please set a contact email address here to help us debug in case of problems (see https://www.uniprot.org/help/privacy). I am not sure you need an email as it worked for both with and withouut"

# This code tells the API we are a human (I am not sure this is needed, as it worked without)
request.add_header('User-Agent', 'Python %s' % contact)

# This code opens the URL with paramters
response = urllib.request.urlopen(request)

# This code reads the details with a limit defined (not sure if this is bytes???)
#page = response.read(200000)

# Print the data (we can also output this as a text file)
   #print(page)

df = pd.read_table(response)
df.to_csv('output4.csv')
