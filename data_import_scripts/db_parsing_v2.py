### Script for importing, filtering & parsing phospho and inhibitor tables.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
import csv
import os.path

# --------------------------------------------------------------------------- #

### Read "Kinase_Substrate_Data" database & convert to data frame.
kin_sub_path = os.path.join('db_source_tables', 'PhosphoSitePlus',
                            'Kinase_Substrate_Dataset')
kin_sub_source_df = pd.read_table(kin_sub_path,
                                  skiprows=3)  # Skip first 3 rows of file.
                                               # PhosphoSitePlus DBs contain
                                               # 3 line info headers.
# --------------------------------------------------------------------------- #
                                               
### Read "Phosphorylation_site_dataset" database & convert to data frame.
phos_sites_path = os.path.join('db_source_tables', 'PhosphoSitePlus',
                               'Phosphorylation_site_dataset')
phos_sites_source_df = pd.read_table(phos_sites_path,
                                     skiprows=3)

# --------------------------------------------------------------------------- #

### Read "Disease-associated_sites" database & convert to data frame.
dis_sites_path = os.path.join('db_source_tables', 'PhosphoSitePlus',
                              'Disease-associated_sites')
dis_sites_source_df = pd.read_table(dis_sites_path,
                                    skiprows=3)

# Remove any rows that have no value in either DISEASE or SITE_GRP_ID
dis_sites_source_df.dropna(subset=['DISEASE', 'SITE_GRP_ID'],
                           inplace=True)

# Change nan to None.
dis_sites_source_df["ALTERATION"] = dis_sites_source_df["ALTERATION"].replace\
                                    ({pd.np.nan: 'unknown'})

# --------------------------------------------------------------------------- #

### Read "Regulatory_sites" database & convert to dataframe.
reg_sites_path = os.path.join('db_source_tables', 'PhosphoSitePlus',
                              'Regulatory_sites')

with open(reg_sites_path) as rsdb:  # Open regulatory sites db.
    rsdb_tbl = []                   # Empty list to append rows from db.
    rd = csv.reader(rsdb,           # Create reader object with db data.
                    delimiter="\t") # Specify table separator.
    for row in rd:                  # Iterate through rows in reader object.
        rsdb_tbl.append(row)        # Append rows to empty list.

# Transform db list object to dataframe from row 4.    
reg_sites_source_df = pd.DataFrame(rsdb_tbl[3:])  
# Define first row as header.
reg_sites_headers = reg_sites_source_df.iloc[0] 
# Define data as table less the header row.  
reg_sites_source_df = reg_sites_source_df[1:]  
# Define header row as the column headers.  
reg_sites_source_df.columns = reg_sites_headers  

# --------------------------------------------------------------------------- #

### Read "BindingDB_BindingDB_inhibition" database & convert to dataframe.
bindingDB_path = os.path.join('db_source_tables', 'BindingDB',
                              'BindingDB_BindingDB_Inhibition.tsv')
with open(bindingDB_path, encoding="Latin-1") as bdb:
    bdb_tbl = []
    rd = csv.reader(bdb, 
                    delimiter="\t")
    for row in rd:
        bdb_tbl.append(row)

# Transform db list object to dataframe.    
bindingDB_source_df = pd.DataFrame(bdb_tbl)  
# Define first row as header.    
bindingDB_headers = bindingDB_source_df.iloc[0]  
# Define data as table less the header row. 
bindingDB_source_df = bindingDB_source_df[1:] 
# Define header row as the column headers.    
bindingDB_source_df.columns = bindingDB_headers
# Replace header spaces with underscore
bindingDB_source_df.columns = bindingDB_source_df.columns.str.replace(" ", "_")  

# Replace column header for target organism, to something more sensible
bindingDB_source_df.rename(columns={"Target_Source_Organism_According_to_"
                                    "Curator_or_DataSource":"ORGANISM"}, 
                           inplace=True)

# --------------------------------------------------------------------------- #  

### Read MRC inhibitor database & convert to data frame.
mrc_inhib_path = os.path.join('db_source_tables', 'MRC_curated_DB',
                              'kinase_inhibitor_list_2019-01-14T19-38-48.csv')
mrc_inhib_source = pd.read_csv(mrc_inhib_path)

# Parse rows that have entries in "Action" field
mrc_inhib_source = mrc_inhib_source[mrc_inhib_source["Action"].notnull()]

# --------------------------------------------------------------------------- # 

### Filter tables for human entries only and pass to variable.

# Parse "Kinase_Substrate_Dataset" db human entries and pass to variable
kin_sub_human = kin_sub_source_df[(kin_sub_source_df.KIN_ORGANISM == "human") & 
                                  (kin_sub_source_df.SUB_ORGANISM == "human")]

# Parse "Phosphorylation_site_dataset" db human entries and pass to variable
phos_sites_human = phos_sites_source_df[(phos_sites_source_df.ORGANISM==\
                                         "human")]

# Parse "Disease-associated_sites" db human entries and pass to variable
dis_sites_human = dis_sites_source_df[(dis_sites_source_df.ORGANISM==\
                                       "human")]

# Parse "Regulatory_sites" db human entries and pass to variable
reg_sites_human = reg_sites_source_df[(reg_sites_source_df.ORGANISM==\
                                       "human")]

# Parse "BindingDB" inhibitor database human entries and pass to variable
bindingDB_human = bindingDB_source_df[(bindingDB_source_df.ORGANISM==\
                                       "Homo sapiens")]

# --------------------------------------------------------------------------- # 