###### API (Application Programming Interface) Documentation

To enable population of the database, we utilised APIs from three different websites:-

i)	**UniProt**

The UniProt website obtained selected data using a kinase or substrate qualifier from the default UniProt site:-

https://www.uniprot.org/uploadlists/

The API obtains a number of parameters, which are selected using specified qualifier names from the UniProtKB column names for programmatic access site:-

https://www.uniprot.org/help/uniprotkb_column_names

To allow population of the database, we have selected the columns:-

'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families,'
                   'genes,proteome,comment(DOMAIN)',

ii)	**PubChem** 

The PubChem website obtained selected data using the CID qualifier from the default PubChem site:-

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/

The API obtains a number of parameters, which are selected using specified qualifier names denoted from the PubChem help site:-

https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

To allow population of the database, we have selected the columns:-

"/property/IUPACName,MolecularFormula,MolecularWeight/csv"
