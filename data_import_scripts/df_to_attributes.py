# import classes
from data_access.sqlalchemy_declarative import Base, Kinase, Substrate, \
    Phosphosite, Disease, DiseaseAlteration, Inhibitor, CellularLocation


# Dictionaries mapping 'DF header' : ('Class', 'class_attribute') #
###################################################################

# PhosphoSitePlus kinase substrate dataset
kin_sub_human_to_class = {
    'GENE'        : (Kinase,      'kin_gene'),
    'KINASE'      : (Kinase,      'kin_short_name'),
    'KIN_ACC_ID'  : (Kinase,      'kin_accession'),
    'KIN_ORGANISM': (Kinase,      'kin_organism'),
    'SUBSTRATE'   : (Substrate,   'subs_short_name'),
    'SUB_ACC_ID'  : (Substrate,   'subs_accession'),
    'SUB_GENE'    : (Substrate,   'subs_gene'),
    'SUB_ORGANISM': (Substrate,   'subs_organism'),
    'SUB_MOD_RSD' : (Phosphosite, 'phos_modified_residue'),
    'SITE_GRP_ID' : (Phosphosite, 'phos_group_id'),
    'SITE_+/-7_AA': (Phosphosite, 'phos_site'),
    'DOMAIN'      : (Phosphosite, 'phos_domain'),
    'CST_CAT#'    : (Phosphosite, 'phos_cst_catalog_number')
}

# PhosphoSitePlus phosphorylation site dataset
phos_sites_human_to_class = {
    'GENE'        : (Substrate,   'subs_gene'),
    'PROTEIN'     : (Substrate,   'subs_short_name'),
    'ACC_ID'      : (Substrate,   'subs_accession'),
    'HU_CHR_LOC'  : (Substrate,   'subs_chrom_location'),
    'MOD_RSD'     : (Phosphosite, 'phos_modified_residue'),
    'SITE_GRP_ID' : (Phosphosite, 'phos_group_id'),
    'ORGANISM'    : (Substrate,   'subs_organism'),
    'MW_kD'       : (Substrate,   'subs_molec_weight_kd'),
    'DOMAIN'      : (Phosphosite, 'phos_domain'),
    'SITE_+/-7_AA': (Phosphosite, 'phos_site'),
    'CST_CAT#'    : (Phosphosite, 'phos_cst_catalog_number')
}

# PhosphoSitePlus regulatory site dataset
reg_sites_human_to_class = {
    'GENE'             : (Substrate,   'subs_gene'),
    'PROTEIN'          : (Substrate,   'subs_short_name'),
    'PROT_TYPE'        : (Substrate,   'subs_protein_type'),
    'ACC_ID'           : (Substrate,   'subs_accession'),
    'HU_CHR_LOC'       : (Substrate,   'subs_chrom_location'),
    'ORGANISM'         : (Substrate,   'subs_organism'),
    'MOD_RSD'          : (Phosphosite, 'phos_modified_residue'),
    'SITE_GRP_ID'      : (Phosphosite, 'phos_group_id'),
    'SITE_+/-7_AA'     : (Phosphosite, 'phos_site'),
    'DOMAIN'           : (Phosphosite, 'phos_domain'),
    'ON_FUNCTION'      : (Phosphosite, 'phos_p_function'),
    'ON_PROCESS'       : (Phosphosite, 'phos_p_processes'),
    'ON_PROT_INTERACT' : (Phosphosite, 'phos_prot_interactions'),
    'ON_OTHER_INTERACT': (Phosphosite, 'phos_other_interactions'),
    'PMIDs'            : (Phosphosite, 'phos_bibl_references'),
    'NOTES'            : (Phosphosite, 'phos_notes')
}

# PhosphoSitePlus disease-associated sites dataset
dis_sites_human_to_class = {
    'DISEASE'     : (DiseaseAlteration, 'disalt_disease_name'),
    'ALTERATION'  : (DiseaseAlteration, 'disalt_phos_alteration'),
    'GENE'        : (Substrate,         'subs_gene'),
    'PROTEIN'     : (Substrate,         'subs_short_name'),
    'ACC_ID'      : (Substrate,         'subs_accession'),
    'HU_CHR_LOC'  : (Substrate,         'subs_chrom_location'),
    'MW_kD'       : (Substrate,         'subs_molec_weight_kd'),
    'ORGANISM'    : (Substrate,         'subs_organism'),
    'SITE_GRP_ID' : (DiseaseAlteration, 'disalt_phosphosite_id'),
    'MOD_RSD'     : (Phosphosite,       'phos_modified_residue'),
    'DOMAIN'      : (Phosphosite,       'phos_domain'),
    'SITE_+/-7_AA': (Phosphosite,       'phos_site'),
    'PMIDs'       : (DiseaseAlteration, 'disalt_bibl_references'),
    'CST_CAT#'    : (Phosphosite,       'phos_cst_catalog_number'),
    'NOTES'       : (DiseaseAlteration, 'disalt_notes'),
}

# MRC inhibitors database
mrc_inhib_source_to_class = {
    'Inhibitor'        : (Inhibitor, 'inhib_short_name'),
    'Brutto'           : (Inhibitor, 'inhib_brutto'),
    'MW'               : (Inhibitor, 'inhib_molec_weight'),
    'Commercial Vendor': (Inhibitor, 'inhib_vendor'),
    'CAS'              : (Inhibitor, 'inhib_catalog_number'),
    'InChI'            : (Inhibitor, 'inhib_int_chem_id'),
    'InChI Key'        : (Inhibitor, 'inhib_int_chem_id_key'),
    'PubChem CID'      : (Inhibitor, 'inhib_pubchem_cid'),
    'SMILES'           : (Inhibitor, 'inhib_smile')
}

bindingDB_human_to_class = {
    'PubChem_CID':
        (Inhibitor, 'inhib_pubchem_cid'),
    'UniProt_(SwissProt)_Primary_ID_of_Target_Chain':
        (Kinase, 'kin_accession')
}

"""
Class attributes
################

kin_accession
kin_short_name
kin_full_name
kin_gene
kin_organism
kin_cellular_location
kin_family

subs_accession
subs_short_name
subs_full_name
subs_protein_type
subs_molec_weight_kd
subs_gene
subs_chrom_location
subs_organism

phos_group_id
phos_modified_residue
phos_site
phos_domain
phos_cst_catalog_number
phos_p_function
phos_p_processes
phos_prot_interactions
phos_other_interactions
phos_bibl_references
phos_notes
phos_in_substrate

dis_name

disalt_disease_name
disalt_phosphosite_id
disalt_phos_alteration
disalt_bibl_references
disalt_notes

inhib_pubchem_cid
inhib_short_name
inhib_full_name
inhib_brutto
inhib_molec_weight
inhib_chem_structure
inhib_smile
inhib_int_chem_id
inhib_int_chem_id_key
inhib_bibl_references
inhib_vendor
inhib_catalog_number

loc_name
loc_image_path


Dataframe fields
################

> Kinase_Substrate_Dataset
GENE
KINASE
KIN_ACC_ID
KIN_ORGANISM
SUBSTRATE
SUB_GENE_ID
SUB_ACC_ID
SUB_GENE
SUB_ORGANISM
SUB_MOD_RSD
SITE_GRP_ID
SITE_ + / -7_AA
DOMAIN
IN_VIVO_RXN
IN_VITRO_RXN
CST_CAT  #

> Phosphorylation site dataset
GENE
PROTEIN
ACC_ID
HU_CHR_LOC
MOD_RSD
SITE_GRP_ID
ORGANISM
MW_kD
DOMAIN
SITE_ + / -7_AA
LT_LIT
MS_LIT
MS_CST
CST_CAT#

> Regulatory sites
GENE
PROTEIN
PROT_TYPE
ACC_ID
GENE_ID
HU_CHR_LOC
ORGANISM
MOD_RSD
SITE_GRP_ID
SITE_+/-7_AA
DOMAIN
ON_FUNCTION
ON_PROCESS
ON_PROT_INTERACT
ON_OTHER_INTERACT
PMIDs
LT_LIT
MS_LIT
MS_CST
NOTES

> Disease-associated sites
DISEASE
ALTERATION
GENE
PROTEIN
ACC_ID
GENE_ID
HU_CHR_LOC
MW_kD
ORGANISM
SITE_GRP_ID
MOD_RSD
DOMAIN
SITE_ + / -7_AA
PubMedIDs
LT_LIT
MS_LIT
MS_CST
CellSignallingTech_CAT  #
NOTES

> MRC inhibitors
CNumber
Inhibitor
Brutto
MW
Action
Reference
Reference 2
Patent
Commercial Vendor
CAS
InChI
InChI Key
PubChem CID
SMILES

> Binding DB
BindingDB_Reactant_set_id
Ligand_SMILES
Ligand_InChI
Ligand_InChI_Key
BindingDB_MonomerID
BindingDB_Ligand_Name
Target_Name_Assigned_by_Curator_or_DataSource
ORGANISM
Ki_(nM)
IC50_(nM)
Kd_(nM)
EC50_(nM)
kon_(M-1-s-1)
koff_(s-1)
pH
Temp_(C)
Curation/DataSource
Article_DOI
PMID
PubChem_AID
Patent_Number
Authors
Institution
Link_to_Ligand_in_BindingDB
Link_to_Target_in_BindingDB
Link_to_Ligand-Target_Pair_in_BindingDB
Ligand_HET_ID_in_PDB
PDB_ID(s)_for_Ligand-Target_Complex
PubChem_CID
PubChem_SID
ChEBI_ID_of_Ligand
ChEMBL_ID_of_Ligand
DrugBank_ID_of_Ligand
IUPHAR_GRAC_ID_of_Ligand
KEGG_ID_of_Ligand
ZINC_ID_of_Ligand
Number_of_Protein_Chains_in_Target_(>1_implies_a_multichain_complex)
BindingDB_Target_Chain__Sequence
PDB_ID(s)_of_Target_Chain
UniProt_(SwissProt)_Recommended_Name_of_Target_Chain
UniProt_(SwissProt)_Entry_Name_of_Target_Chain
UniProt_(SwissProt)_Primary_ID_of_Target_Chain
UniProt_(SwissProt)_Secondary_ID(s)_of_Target_Chain
UniProt_(SwissProt)_Alternative_ID(s)_of_Target_Chain
UniProt_(TrEMBL)_Submitted_Name_of_Target_Chain
UniProt_(TrEMBL)_Entry_Name_of_Target_Chain
UniProt_(TrEMBL)_Primary_ID_of_Target_Chain
UniProt_(TrEMBL)_Secondary_ID(s)_of_Target_Chain
UniProt_(TrEMBL)_Alternative_ID(s)_of_Target_Chain

"""