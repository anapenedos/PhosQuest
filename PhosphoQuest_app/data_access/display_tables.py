from flask_table import Table, Col, LinkCol

# Tables for browse and search results

class Kinase_first_results(Table):
    """create Kinase results part info table format"""
    kin_accession = Col('Accession no')
    kin_full_name = Col('Full name')
    kin_gene = Col('Gene')
    detail = LinkCol('Detail', 'browse.kin_detail',
                            url_kwargs=dict(text='kin_accession'))

class Substrate_first_results(Table):
    """create Substrates part info  results table format"""
    subs_accession = Col('Accession no')
    subs_full_name = Col('Full name')
    subs_molec_weight_kd = Col('Molecular weight (kd)')
    subs_gene = Col('Gene')
    subs_chrom_location = Col('Chromosome location')
    detail = LinkCol('Detail', 'browse.sub_detail',
                     url_kwargs=dict(text='subs_accession'))

class Inhibitor_first_results(Table):
    """create table of inhibitors for first result display"""
    inhib_pubchem_cid = Col('PubChem no')
    inhib_short_name = Col('Short name')
    inhib_brutto = Col('Brutto')
    inhib_molec_weight = Col('Molecular Weight')
    inhib_vendor = Col('Vendor')
    inhib_catalog_number = Col('Cat. No')
    detail = LinkCol('Detail', 'browse.inh_detail',
                     url_kwargs=dict(text='inhib_pubchem_cid'))

class Phosphosites(Table):
    """create table of Phosphosites related to substrate"""
    phos_group_id = Col('Group ID')
    phos_modified_residue = Col('Modified Residue')
    phos_site = Col('Phosphorylation Site')
    phos_domain = Col('Domain')
    phos_p_function = Col('Function')
    detail = LinkCol('Detail', 'browse.phosites_detail',
                     url_kwargs=dict(text='phos_group_id'))
