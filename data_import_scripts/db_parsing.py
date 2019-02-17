### Script for importing, filtering & parsing phospho and inhibitor tables.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
import csv
import os.path

# --------------------------------------------------------------------------- #

### Function to generate kinase/substrate data frame.
def kin_sub_import(path):
    """ Read data and parse human entries. """
    # Define path variable.
    # "path" is a string, which is split at ",".
    # Note: list of strings returned.
    path_var = path.split(",")
    
    # Define path to source data-base.
    # Note: "*" before path triggers unpacking of list, to a single
    # string of the correct format to pass to "os.path.join".
    db_path = os.path.join(*path_var)
    
    # Read data-base and pass to data frame.
    db_df = pd.read_table(db_path, skiprows=3) # Skip 1st 3 rows
                                               # 3 line info headers.
                                           
    # Parse db human entries and pass to variable.
    db_human = db_df[(db_df.KIN_ORGANISM == "human") &
                     (db_df.SUB_ORGANISM == "human")]
    
    return db_human     
              
# --------------------------------------------------------------------------- #

### Function to generate phospho-site data frame.
def phos_site_import(path):
    """ Read data and parse human entries. """
    # Define path variable.
    # "path" is a string, which is split at ",".
    # Note: list of strings returned.
    path_var = path.split(",")
    
    # Define path to source data-base.
    # Note: "*" before path triggers unpacking of list, to a single
    # string of the correct format to pass to "os.path.join".
    db_path = os.path.join(*path_var)
    
    # Read data-base and pass to data frame.
    db_df = pd.read_table(db_path, skiprows=3)
                                           
    # Parse db human entries and pass to variable.
    db_human = db_df[(db_df.ORGANISM == "human")]

    return db_human                                                 

# --------------------------------------------------------------------------- #

### Function to generate disease-sites data frame.
def dis_site_import(path):
    """ Read data and parse human entries. """
    # Define path variable.
    # "path" is a string, which is split at ",".
    # Note: list of strings returned.
    path_var = path.split(",")
    
    # Define path to source data-base.
    # Note: "*" before path triggers unpacking of list, to a single
    # string of the correct format to pass to "os.path.join".
    db_path = os.path.join(*path_var)
    
    # Read data-base and pass to data frame.
    db_df = pd.read_table(db_path, skiprows=3)
                                      
    # Remove any rows that have no value in either DISEASE or SITE_GRP_ID
    db_df.dropna(subset=['DISEASE', 'SITE_GRP_ID'], inplace=True)
    
    # Change nan in 'ALTERATION' to 'unknown'.
    db_df["ALTERATION"] = db_df["ALTERATION"].replace({pd.np.nan: 'unknown'}) 
    
    # Change dtype in 'PMIDs' and 'SITE_GRP_ID' to integer
    db_df[['PMIDs', 'SITE_GRP_ID']] = db_df[['PMIDs', 'SITE_GRP_ID']].\
                                             astype(int)                                
    # Parse db human entries and pass to variable.
    db_human = db_df[(db_df.ORGANISM == "human")]

    return db_human 

# --------------------------------------------------------------------------- #
    
### Function to generate regulatory-sites data frame.
def reg_site_import(path):
    """ Read data and parse human entries. """
    # Define path variable.
    # "path" is a string, which is split at ",".
    # Note: list of strings returned.
    path_var = path.split(",")
    
    # Define path to source data-base.
    # Note: "*" before path triggers unpacking of list, to a single
    # string of the correct format to pass to "os.path.join".
    db_path = os.path.join(*path_var)
    
    with open(db_path) as rsdb:     # Open regulatory sites db.
        rsdb_tbl = []               # Empty list to append rows from db.
        rd = csv.reader(rsdb,       # Create reader object with db data.
                    delimiter="\t") # Specify table separator.
        for row in rd:              # Iterate through rows in reader object.
            rsdb_tbl.append(row)    # Append rows to empty list.

    # Transform db list object to dataframe from row 4.    
    db_df = pd.DataFrame(rsdb_tbl[3:])  
    # Define first row as header.
    db_df_headers = db_df.iloc[0] 
    # Define data as table less the header row.  
    db_df = db_df[1:]  
    # Define header row as the column headers.  
    db_df.columns = db_df_headers
    
    # Change dtype in 'SITE_GRP_ID' to integer
    db_df[['SITE_GRP_ID']] = db_df[['SITE_GRP_ID']].astype(int)
                                                                      
    # Parse db human entries and pass to variable.
    db_human = db_df[(db_df.ORGANISM == "human")]
    
    # Parse sites with only phospho as modification.
    # Note - column "MOD-RSD" entries with extension to string = "-p".
    # Regex - parse lines that end with "-p".
    db_human_phos = \
        db_human[db_human.iloc[:, 7].str.contains(r"-p$", regex=True)]
        
    # Remove "-p" extension to entries.
    db_human_phos.iloc[:, 7] = db_human_phos.iloc[:, 7].str.replace("-p", "")

    return db_human_phos

# --------------------------------------------------------------------------- #

### Function to generate BindingDb inhibitor data frame.
def bdb_inhib_import(path):
    """ Read data and parse human entries. """
    # Define path variable.
    # "path" is a string, which is split at ",".
    # Note: list of strings returned.
    path_var = path.split(",")
    
    # Define path to source data-base.
    # Note: "*" before path triggers unpacking of list, to a single
    # string of the correct format to pass to "os.path.join".
    db_path = os.path.join(*path_var)
    
    with open(db_path, encoding="Latin-1") as bdb:
        bdb_tbl = []
        rd = csv.reader(bdb, 
                        delimiter="\t")
        for row in rd:
            bdb_tbl.append(row)

    # Transform db list object to dataframe.    
    db_df = pd.DataFrame(bdb_tbl)  
    # Define first row as header.    
    db_df_headers = db_df.iloc[0]  
    # Define data as table less the header row. 
    db_df = db_df[1:] 
    # Define header row as the column headers.    
    db_df.columns = db_df_headers
    # Replace header spaces with underscore
    db_df.columns = db_df.columns.str.replace(" ", "_")  

    # Replace column header for target organism, to something more sensible.
    db_df.rename(columns={"Target_Source_Organism_According_to_"
                          "Curator_or_DataSource":"ORGANISM"}, 
                           inplace=True)
    
    # Remove lines without PubChem CID
    db_df = db_df[db_df.PubChem_CID != '']
    
    # set PubChem CID to integer
    db_df[['PubChem_CID']] = db_df[['PubChem_CID']].astype(int)
    
    # Parse db human entries and pass to variable.
    db_human = db_df[(db_df.ORGANISM == "Homo sapiens")]

    return db_human     

# --------------------------------------------------------------------------- #  

### Function to generate MRC inhibitor data frame.
def mrc_inhib_import(path):
    """ Read data and parse entries. """
    # Define path variable.
    # "path" is a string, which is split at ",".
    # Note: list of strings returned.
    path_var = path.split(",")
    
    # Define path to source data-base.
    # Note: "*" before path triggers unpacking of list, to a single
    # string of the correct format to pass to "os.path.join".
    db_path = os.path.join(*path_var)
    
    db_df = pd.read_csv(db_path)

    # Parse rows that have entries in "Action" field.
    db_df = db_df[db_df["Action"].notnull()]
    # Parse rows that have entries in "PubChem CID" field.
    db_df = db_df[db_df["PubChem CID"].notnull()]
    # Change dtype in 'PubChem CID' to integer.
    db_df[['PubChem CID']] = db_df[['PubChem CID']].astype(int)
    # Change dtype of 'MW' to float.
    db_df[['MW']] = db_df[['MW']].astype(float)

    return db_df     

# --------------------------------------------------------------------------- # 

### Call functions for import data-bases.

# Human kinase/substrate db as data frame.
kin_sub_human = kin_sub_import("db_source_tables,"
                               "PhosphoSitePlus,"
                               "Kinase_Substrate_Dataset")


# Human phospho-site db as data frame.
phos_sites_human = phos_site_import("db_source_tables,"
                                    "PhosphoSitePlus,"
                                    "Phosphorylation_site_dataset")

# Human disease-site db as data frame.
dis_sites_human = dis_site_import("db_source_tables,"
                                  "PhosphoSitePlus,"
                                  "Disease-associated_sites")


# Human regulatory-site db as data frame.
reg_sites_human = reg_site_import("db_source_tables,"
                                  "PhosphoSitePlus,"
                                  "Regulatory_sites")


# Human BindingDB as data frame.
bindingDB_human = bdb_inhib_import("db_source_tables,"
                                   "BindingDB,"
                                   "BindingDB_BindingDB_Inhibition.tsv")

mrc_inhib_source = mrc_inhib_import("db_source_tables,"
                                    "MRC_curated_DB,"
                                    "kinase_inhibitor_list_2019-01-14T19-38-48.csv")

# --------------------------------------------------------------------------- # 