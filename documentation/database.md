# The database
## Tools
The DB was setup in SQLite (version 3). SqLite is suitable to low- to 
medium-traffic websites and the one file approach of this type of DBs makes them 
reliable and portable. Its limitations in terms of user management and 
performance optimisation are unlikely to be felt in this project.

Python library SQLalchemy was employed to create and populate the DB. This makes
the PhosphoQuest DB and WebApp more portable and allows for performance 
improvements in the python-SQLite interactions. With SQLalchemy, the DB can be 
transferred to other DB systems, with minimal changes to the 
`sqlalchemy_declarative` (table changes), `db_sessions` (DB path and connections) 
and `db_setup` (creation of tables and data import) scripts, all in the 
`data_import_scripts` directory.

## Database structure
The PhosphoQuest database contains nine tables as outlines in the schema below:
![PhosphoQuest schema](images/PhosphoQuest_schema.png)
The schema is defined through a SQLalchemy declarative script, 
[sqlalchemy_declarative.py](../PhosphoQuest_app/data_access/sqlalchemy_declarative.py)
 

## Data Sources
### Database exports
All external datasets downloaded as files were saved in the `db_source_tables`
directory, under the relevant sub-directory.
Data on kinases, substrates, phosphosites, phosphosite regulation and 
disease-associated alterations was obtained from 
[PhosphoSitePlus](https://www.phosphosite.org/staticDownloads). Files 
`Disease-associated_sites.gz`, `Kinase_Substrate_Dataset.gz`, 
`Phosphorylation_site_dataset.gz`, and `Regulatory_sites.gz` were used to populate 
database tables `kinases`, `substrates`, `phosphosites`, `disease_alterations`, 
and `diseases`. The files were downloaded from the `Downloads` tab, 
`Datasets from PSP` page on _**X/X/XX**_ (last updated 04/03/2019).  
Inhibitor data was obtained from 
[MRC Kinase Profiling Inhibitor Database](http://www.kinase-screen.mrc.ac.uk/kinase-inhibitors)
as a `.csv` file on _**X/X/XX**_ and from 
[BindingDB](https://www.bindingdb.org/bind/chemsearch/marvin/SDFdownload.jsp?all_download=yes) 
as a `zip` compressed `.tsv` file on _**X/X/XX**_ (last updated 08/07/2018) 
(`Full BindingDB Database Dump` option). Given BindingDB's file size, it could 
not be added in its uncompressed form to the github repo due to the latter's file 
size restrictions.
### Application Programming Interface (API) Documentation
API functionality was dependent on the pandas module to allow handling of data 
structures. The API scripts were also dependent on the urllib module to allow 
utilization of URLs. For our database, we required access to UniProt and PubChem 
websites with the ability to search multiple accession numbers and output as a 
dataframe for population of the SQLite database. 

To enable population of the database, we utilised APIs from three different 
websites:

####	UniProt

The UniProt website obtains specific data using a kinase or substrate qualifier 
from the default UniProt site: 

https://www.uniprot.org/uploadlists/

The API uses a number of parameters which are selected when performing a search:

- The ability to convert to another identifier type from your original input type 
is an option. The default here is the ACC abbreviation which is the UniProtKB AC 
category. 
- The return format is in tab form.
- The columns denote the categories of information which can be retrieved. The 
UniProtKB column names for programmatic access can be found 
[here](https://www.uniprot.org/help/uniprotkb_column_names).

To allow population of the database, we have selected as a default the following 
qualifiers:

'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families,'
                   'genes,proteome,comment(DOMAIN)',

- The final qualifier is the accession number itself.

In terms of functionality, the code:

i) Takes parameters and encodes them in a URL format.

ii) Changes to utf-8 format.

iii) Requests the URL and paramters (stored as data) using urllib.request.

iv) Opens the respective URL with parameters and stores as a response variable.

v) Places the retrieved data into a dataframe.

Based on the information retrieved, one of parameters we require to populate our 
database is the subcellular location. This qualifier returns multiple pieces of 
information relating to the subcellular location and here we only wish to retrieve 
the first set of information, the subcellular location. We create a separate 
column and using regular expression extract this information. This is also 
repeated for gene names where we only take the first instance. 

####	PubChem 

To access data from the PubChem website, we have utilised the PubChem REST-style 
version of PUG (Power User Gateway) utility which is a web interface for accessing 
PubChem data and services. To access the data, a URL with a specific structure is 
required: 

- The URL has three parts – input, operation, and output: 

https://pubchem.ncbi.nlm.nih.gov/rest/pug/*input specification*/*operation specification*/*output specification*/*operation_options*

In our case, the selected data was obtained using the CID qualifier from the 
[PubChem site](https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/).

This API allows a number of qualifiers to be retrieved. The full lit can be 
accessed from the following website: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

To allow population of the database, we have selected the columns:

i) IUPACName

ii) MolecularFormula

iii) MolecularWeight

For our searches, the following example was utilized:

results_csv = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
                       "cid/" + query_str + "/property/IUPACName,MolecularFormula,MolecularWeight/csv")
        
Where 'query_str' denotes the CID qualifier. The data was then converted from csv 
to a dataframe ready for population of the SQLite database.          
        
## Database setup