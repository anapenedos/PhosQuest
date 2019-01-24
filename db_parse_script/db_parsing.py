##############################################################################
### Script for importing, filtering & parsing phospho and inhibitor tables ###
##############################################################################

##-------------------------------------------------------------------------------------------------------------------------##

# Import package "pandas" into environment as pd
# Import packages "csv" into environment
import pandas as pd
import csv

##-------------------------------------------------------------------------------------------------------------------------##

################################################
### Read databases and convert to dataframes ###
################################################

### Read "Kinase_Substrate_Data" source database and assign to dataframe variable ###
kin_sub_source_df = pd.read_table("../db_parsing_script/Kinase_Substrate_Dataset", 
                               skiprows=3)  # Skip first 3 rows of file
                                            # PhosphoSitePlus DBs contain 3 line info headers

### Read "Phosphorylation_site_dataset" source database and assign to dataframe variable ###
phos_sites_source_df = pd.read_table("../db_parsing_script/Phosphorylation_site_dataset", 
                                  skiprows=3)

### Read "Disease-associated_sites" source database and assign to dataframe variable ###
dis_sites_source_df = pd.read_table("../db_parsing_script/Disease-associated_sites", 
                                 skiprows=3)

### Read "Regulatory_sites" source database and assign to dataframe variable ###
with open("Regulatory_sites") as rsdb:  # Open regulatory sites db
    rsdb_tbl = []                       # Empty list to append rows from db
    rd = csv.reader(rsdb,               # Create reader object with db data
                    delimiter="\t")     # Specify table separator
    for row in rd:                      # Iterate through rows in reader object
        rsdb_tbl.append(row)            # Append rows to empty list
    
reg_sites_source_df = pd.DataFrame(rsdb_tbl[3:])  # Transform db list object to dataframe from row 4
reg_sites_headers = reg_sites_source_df.iloc[0]   # Define first row as header
reg_sites_source_df = reg_sites_source_df[1:]     # Define data as table less the header row
reg_sites_source_df.columns = reg_sites_headers   # Define header row as the column headers

### Read "BindingDB_BindingDB_inhibition" database and assign to variable ###
with open("BindingDB_BindingDB_Inhibition.tsv", encoding="Latin-1") as bdb:
    bdb_tbl = []
    rd = csv.reader(bdb, 
                    delimiter="\t")
    for row in rd:
        bdb_tbl.append(row)
    
bindingDB_source_df = pd.DataFrame(bdb_tbl)      
bindingDB_headers = bindingDB_source_df.iloc[0]  
bindingDB_source_df = bindingDB_source_df[1:]    
bindingDB_source_df.columns = bindingDB_headers

# Replace headers spaces with underscore
bindingDB_source_df.columns = bindingDB_source_df.columns.str.replace(" ", "_")  

# Replace column header for target organism to something more sensible
bindingDB_source_df.rename(columns={"Target_Source_Organism_According_to_Curator_or_DataSource":"ORGANISM"}, 
                           inplace=True)
  

### Read "kinase_inhibitor_list_2019-01-14T19-38-48" MRC source database and assign to variable ###
mrc_inhib_source = pd.read_csv("../db_parsing_script/kinase_inhibitor_list_2019-01-14T19-38-48.csv")

##-------------------------------------------------------------------------------------------------------------------------##

#################################################################
### Filter tables for human entries only and pass to variable ###
#################################################################

# Parse "Kinase_Substrate_Dataset" db human entries and pass to variable
kin_sub_human = kin_sub_source_df[(kin_sub_source_df.KIN_ORGANISM == "human") & (kin_sub_source_df.SUB_ORGANISM == "human")]

# Parse "Phosphorylation_site_dataset" db human entries and pass to variable
phos_sites_human = phos_sites_source_df[(phos_sites_source_df.ORGANISM == "human")]

# Parse "Disease-associated_sites" db human entries and pass to variable
dis_sites_human = dis_sites_source_df[(dis_sites_source_df.ORGANISM == "human")]

# Parse "Regulatory_sites" db human entries and pass to variable
reg_sites_human = reg_sites_source_df[(reg_sites_source_df.ORGANISM == "human")]

# Parse "BindingDB" inhibitor database human entries and pass to variable
bindingDB_human = bindingDB_source_df[(bindingDB_source_df.ORGANISM == "Homo sapiens")]

##-------------------------------------------------------------------------------------------------------------------------##

####################################################################################
### Extract max length of strings in database dataframe columns - for sqlalchemy ###
####################################################################################

### KINASE/SUBSTRATE DATAFRAME ###

# Kinase accession number
kin_acc_num_len = int(kin_sub_human["KIN_ACC_ID"].str.encode(encoding='utf-8').str.len().max())

# Kinase name
kin_name_len = int(kin_sub_human["KINASE"].str.encode(encoding='utf-8').str.len().max())

# Kinase gene
kin_gene_len = int(kin_sub_human["GENE"].str.encode(encoding='utf-8').str.len().max())

# Substrate accession number
subs_acc_num_len = int(kin_sub_human["SUB_ACC_ID"].str.encode(encoding='utf-8').str.len().max())

# Substrate name
subs_name_len = int(kin_sub_human["SUBSTRATE"].str.encode(encoding='utf-8').str.len().max())

# Substrate gene
subs_gene_len = int(kin_sub_human["SUB_GENE"].str.encode(encoding='utf-8').str.len().max())

# Substrate modified residue
subs_mod_res_len = int(kin_sub_human["SUB_MOD_RSD"].str.encode(encoding='utf-8').str.len().max())

# Substrate domain
subs_domain_len = int(kin_sub_human["DOMAIN"].str.encode(encoding='utf-8').str.len().max())

# Substrate site motif +/- 7 amino acid residues
subs_motif_len = int(kin_sub_human["SITE_+/-7_AA"].str.encode(encoding='utf-8').str.len().max())

# Substrate Cell Signalling Technology antibody cat#
subs_ab_len = int(kin_sub_human["CST_CAT#"].str.encode(encoding='utf-8').str.len().max())
                                       
### PHOSPHO SITES DATAFRAME ###

# Phospho site group ID                                
phos_categ_id_len = int(phos_sites_human["SITE_GRP_ID"].str.encode(encoding='utf-8').str.len().max()) 

# Phospho site
phos_site_len = int(phos_sites_human["MOD_RSD"].str.encode(encoding='utf-8').str.len().max())

# Human chromosome location
phos_genomic_loc_len = int(phos_sites_human["HU_CHR_LOC"].str.encode(encoding='utf-8').str.len().max())

### MRC INHIBITOR DATABASE ###

# Inhibitor ID
# ok who wants a go? I can't work it out...grrrhhh

# Molecular formula
inhib_chem_struct_len = int(mrc_inhib_source["Brutto"].str.encode(encoding='utf-8').str.len().max())

# Inhibitor name
inhib_name_len = int(mrc_inhib_source["Inhibitor"].str.encode(encoding='utf-8').str.len().max())

##-------------------------------------------------------------------------------------------------------------------------##


                      
                                      
