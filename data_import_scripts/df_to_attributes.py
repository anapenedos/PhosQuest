# import classes
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Phosphosite, Disease, DiseaseAlteration, Inhibitor, \
    CellularLocation

# Dictionaries mapping 'DF header' : [('Class', 'class_attribute')] #
#####################################################################

# PhosphoSitePlus kinase substrate dataset
kin_sub_human_to_class = {
    'GENE'        : [(Kinase,      'kin_gene')],
    'KINASE'      : [(Kinase,      'kin_name')],
    'KIN_ACC_ID'  : [(Kinase,      'kin_accession')],
    'KIN_ORGANISM': [(Kinase,      'kin_organism')],
    'SUBSTRATE'   : [(Substrate,   'subs_name')],
    'SUB_ACC_ID'  : [(Substrate,   'subs_accession')],
    'SUB_GENE'    : [(Substrate,   'subs_gene')],
    'SUB_ORGANISM': [(Substrate,   'subs_organism')],
    'SUB_MOD_RSD' : [(Phosphosite, 'phos_modified_residue')],
    'SITE_GRP_ID' : [(Phosphosite, 'phos_group_id')],
    'SITE_+/-7_AA': [(Phosphosite, 'phos_site')],
    'DOMAIN'      : [(Phosphosite, 'phos_domain')],
    'CST_CAT#'    : [(Phosphosite, 'phos_cst_catalog_number')]
}

# PhosphoSitePlus phosphorylation site dataset
phos_sites_human_to_class = {
    'GENE'        : [(Substrate,   'subs_gene')],
    'PROTEIN'     : [(Substrate,   'subs_name')],
    'ACC_ID'      : [(Substrate,   'subs_accession')],
    'HU_CHR_LOC'  : [(Substrate,   'subs_chrom_location')],
    'MOD_RSD'     : [(Phosphosite, 'phos_modified_residue')],
    'SITE_GRP_ID' : [(Phosphosite, 'phos_group_id')],
    'ORGANISM'    : [(Substrate,   'subs_organism')],
    'MW_kD'       : [(Substrate,   'subs_molec_weight_kd')],
    'DOMAIN'      : [(Phosphosite, 'phos_domain')],
    'SITE_+/-7_AA': [(Phosphosite, 'phos_site')],
    'CST_CAT#'    : [(Phosphosite, 'phos_cst_catalog_number')]
}

# PhosphoSitePlus regulatory site dataset
reg_sites_human_to_class = {
    'GENE'             : [(Substrate,   'subs_gene')],
    'PROTEIN'          : [(Substrate,   'subs_name')],
    'PROT_TYPE'        : [(Substrate,   'subs_protein_type')],
    'ACC_ID'           : [(Substrate,   'subs_accession')],
    'HU_CHR_LOC'       : [(Substrate,   'subs_chrom_location')],
    'ORGANISM'         : [(Substrate,   'subs_organism')],
    'MOD_RSD'          : [(Phosphosite, 'phos_modified_residue')],
    'SITE_GRP_ID'      : [(Phosphosite, 'phos_group_id')],
    'SITE_+/-7_AA'     : [(Phosphosite, 'phos_site')],
    'DOMAIN'           : [(Phosphosite, 'phos_domain')],
    'ON_FUNCTION'      : [(Phosphosite, 'phos_p_function')],
    'ON_PROCESS'       : [(Phosphosite, 'phos_p_processes')],
    'ON_PROT_INTERACT' : [(Phosphosite, 'phos_prot_interactions')],
    'ON_OTHER_INTERACT': [(Phosphosite, 'phos_other_interactions')],
    'PMIDs'            : [(Phosphosite, 'phos_bibl_references')],
    'NOTES'            : [(Phosphosite, 'phos_notes')]
}

# PhosphoSitePlus disease-associated sites dataset
dis_sites_human_to_class = {
    'DISEASE'     : [(Disease,           'dis_name'),
                     (DiseaseAlteration, 'disalt_disease_name')],
    'ALTERATION'  : [(DiseaseAlteration, 'disalt_phos_alteration')],
    'GENE'        : [(Substrate,         'subs_gene')],
    'PROTEIN'     : [(Substrate,         'subs_name')],
    'ACC_ID'      : [(Substrate,         'subs_accession')],
    'HU_CHR_LOC'  : [(Substrate,         'subs_chrom_location')],
    'MW_kD'       : [(Substrate,         'subs_molec_weight_kd')],
    'ORGANISM'    : [(Substrate,         'subs_organism')],
    'SITE_GRP_ID' : [(Phosphosite,       'phos_group_id'),
                     (DiseaseAlteration, 'disalt_phosphosite_id')],
    'MOD_RSD'     : [(Phosphosite,       'phos_modified_residue')],
    'DOMAIN'      : [(Phosphosite,       'phos_domain')],
    'SITE_+/-7_AA': [(Phosphosite,       'phos_site')],
    'PMIDs'       : [(DiseaseAlteration, 'disalt_bibl_references')],
    'CST_CAT#'    : [(Phosphosite,       'phos_cst_catalog_number')],
    'NOTES'       : [(DiseaseAlteration, 'disalt_notes')]
}

# MRC inhibitors database
mrc_inhib_source_to_class = {
    'Inhibitor'        : [(Inhibitor, 'inhib_name')],
    'Brutto'           : [(Inhibitor, 'inhib_molec_formula')],
    'MW'               : [(Inhibitor, 'inhib_molec_weight')],
    'Commercial Vendor': [(Inhibitor, 'inhib_vendor')],
    'CAS'              : [(Inhibitor, 'inhib_catalog_number')],
    'InChI'            : [(Inhibitor, 'inhib_int_chem_id')],
    'InChI Key'        : [(Inhibitor, 'inhib_int_chem_id_key')],
    'PubChem CID'      : [(Inhibitor, 'inhib_pubchem_cid')],
    'SMILES'           : [(Inhibitor, 'inhib_smile')]
}

bindingDB_human_to_class = {
    'PubChem_CID'          : [(Inhibitor, 'inhib_pubchem_cid')],
    'Ligand_SMILES'        : [(Inhibitor, 'inhib_smile')],
    'Ligand_InChI'         : [(Inhibitor, 'inhib_int_chem_id')],
    'Ligand_InChI_Key'     : [(Inhibitor, 'inhib_int_chem_id_key')],
    'Target_Name_Assigned_by_Curator_or_DataSource' :
                             [(Kinase,    'kin_full_name')],
    'BindingDB_Ligand_Name': [(Inhibitor, 'inhib_name')],
    'PMID'                 : [(Inhibitor, 'inhib_bibl_references')],
    'UniProt_(SwissProt)_Primary_ID_of_Target_Chain':
                             [(Kinase,    'kin_accession')],
}

uniprot_kin_to_class = {
    'Entry'               : [(Kinase,           'kin_accession')],
    'Subcellular location': [(Kinase,           'kin_cellular_location'),
                             (CellularLocation, 'loc_name')],
    'Protein name'        : [(Kinase,           'kin_full_name')],
    'Protein families'    : [(Kinase,           'kin_family')],
    'Genes'               : [(Kinase,           'kin_gene')]
}

uniprot_subs_to_class = {
    'Entry'           : [(Substrate,        'subs_accession')],
    'Protein name'    : [(Substrate,        'subs_full_name')],
    'Protein families': [(Substrate,        'subs_protein_type')],
    'Genes'           : [(Substrate,        'subs_gene')]
}

pubchem_to_class = {
    'CID'             : [(Inhibitor, 'inhib_pubchem_cid')],
    'IUPACName'       : [(Inhibitor, 'inhib_compound')],
    'MolecularWeight' : [(Inhibitor, 'inhib_molec_weight')],
    'MolecularFormula': [(Inhibitor, 'inhib_molec_formula')]
}
