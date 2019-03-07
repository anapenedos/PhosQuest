"""script to contain dictionaries and lists used for interface
 translation or browsing"""

#database table field headers for interface display
headers = {
    'kin_accession':'Accession no', 'kin_short_name':'Short name',
    'kin_full_name' :'Full name', 'kin_gene':'Gene',
    'kin_organism':'Species', 'kin_cellular_location':'Cellular location',
    'kin_family': 'Family', 'subs_accession':'Accession no',
    'subs_short_name':'Short name', 'subs_full_name':'Full name',
    'subs_protein_type':'Protein type',
              'subs_molec_weight_kd':'Molecular weight (kd)',
    'subs_gene':'Gene', 'subs_chrom_location':'Chromosome location',
    'subs_organism':'Species', 'phos_group_id':'Group ID',
    'phos_modified_residue': 'Modified residue','phos_site':'Phosphosite',
    'phos_domain':'Phosphorylation domain',
              'phos_cst_catalog_number':'CST Catalog number',
    'phos_p_function':'Phosphorylation Function',
    'phos_p_processes':'Processes',
        'phos_prot_interactions':'Protein Interactions',
    'other_interactions':'Other interactions',
    'phos_bibl_references':'References','phos_notes':'Notes',
    'phos_in_substrate':'In substrate',
    'inhib_pubchem_cid':'PubChem CID', 'inhib_short_name':'Short name',
    'inhib_full_name':'Full name', 'inhib_brutto':'Brutto',
    'inhib_molec_weight':'molec. weight (g/mol)', 'inhib_smile':'SMILE',
    'inhib_int_chem_id':'InChI', 'inhib_int_chem_id_key':'InChI key',
    'inhib_bibl_references':'References', 'inhib_vendor':'vendor',
    'inhib_catalog_number':'Cat. No.'

}

#Location categories for Browse etc
location_cats = ['Acrosome', 'Axon', 'Caveola','Cell cortex', 'Cell junction',
                 'Cell projection', 'Centriole', 'Centromere', 'Chromosome',
                 'Cilium', 'Cytoplasm', 'Cytoskeleton', 'Cytosol', 'Dendrite',
                 'Endoplasmic reticulum', 'Endosome', 'Extracellular',
                 'Golgi apparatus', 'Lysosome', 'Melanosome', 'Microsome',
                 'Midbody', 'Mitochondrion', 'Nucleus', 'Perinuclear',
                 'PML body', 'Ruffle', 'Sarcolemma', 'Secreted',
                 'Secretory vesicle', 'Spindle', 'Synapse']

kin_family_cats = ["5'-AMP-activated protein kinase beta subunit",
                "5'-AMP-activated protein kinase gamma subunit",
                "AGC Ser/Thr protein kinase","Alpha-type protein kinase",
                "BUD32","CAMK Ser/Thr protein kinase",
                "Casein kinase 2 subunit beta",
                "CK1 Ser/Thr protein kinase", "CMGC Ser/Thr protein kinase",
                "FAM20","Gfo/Idh/MocA", "Heat shock protein 70",
                "Myosin; Protein kinase superfamily", "NDK",
                "NEK Ser/Thr protein kinase",
                "Nucleotide pyrophosphatase/phosphodiesterase",
                "PDK/BCKDK protein kinase", "Phosphoglycerate kinase",
                "Phosphorylase b kinase regulatory chain", "PI3/PI4-kinase",
                "Pyruvate kinase", "RIO-type Ser/Thr kinase",
                "Ser/Thr protein kinase", "STE Ser/Thr protein kinase","TAF1",
                "TFIIF alpha subunit", "TKL Ser/Thr protein kinase",
                "TRAFAC class myosin-kinesin ATPase superfamily",
                "Transglutaminase","Tyr protein kinase", "WAL"]
