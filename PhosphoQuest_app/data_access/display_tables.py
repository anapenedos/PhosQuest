from flask_table import Table, Col, LinkCol

class Kinase_first_results(Table):
    """create Kinase results part info table format"""
    kin_accession = Col('Accession no')
    kin_full_name = Col('Full name')
    kin_gene = Col('Gene')
    detail = LinkCol('Detail', 'browse.kin_detail',
                            url_kwargs=dict(text='kin_accession'))


class Inhibitor_first_results(Table):
    """create table of buttons for subcats"""

    inhib_pubchem_cid = Col('PubChem no')
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

# class Substrate_full_results(Table):
#     """create Substrates full info results table format"""
#     subs_accession = Col('Accession no')
#     subs_short_name = Col('Short name')
#     subs_full_name = Col('Full name')
#     subs_protein_type = Col('Protein type')
#     subs_molec_weight_kd = Col('Molecular weight (kd)')
#     subs_gene = Col('Gene')
#     subs_chrom_location = Col('Chromosome location')
#     subs_organism = Col('Species')
#     detail = LinkCol('Detail', 'browse.sub_detail',
#                      url_kwargs=dict(text='subs_accession'))
#
# class Kinase_full_results(Table):
#     """create Kinase results full info table format"""
#     kin_accession = Col('Accession no')
#     kin_short_name = Col('Short name')
#     kin_full_name = Col('Full name')
#     kin_gene = Col('Gene')
#     kin_organism = Col('Species')
#     kin_cellular_location = Col('Cellular location')
#     kin_family = Col('Family')
#     detail = LinkCol('Detail', 'browse.kin_detail',
#                          url_kwargs=dict(text='kin_accession'))