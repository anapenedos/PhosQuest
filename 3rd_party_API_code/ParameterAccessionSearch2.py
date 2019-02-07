### The following code has the following features:-
### Uses the uniprot.org/uniprot website
### Saves to output2.txt, but unstructured output
### Only works with one Accession number

### Import modules (I am not sure you need this module as it works without also, but some guides included it)
import urllib.request
import urllib.parse

try:

# The default base URL
    url = 'https://www.uniprot.org/uniprot/'

# Example parameters
    params = {
        #'from':'ACC',
        #'to':'ID',
        'format':'tab',
        'columns':'accession name,database(PDB),comment(SUBCELLULAR LOCATION),feature(INTRAMEMBRANE),feature(TOPOLOGICAL DOMAIN),feature(TRANSMEMBRANE)',
        'query':'G1FDY4'
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
    page = response.read(200000)

# Print the data (we can also output this as a text file)
#print(page)

    saveFile = open('output2.csv', 'w')
    saveFile.write(str(page))
    saveFile.close()

except Exception as e:
    print (str(e))
