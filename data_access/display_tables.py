from flask_table import Table, Col, LinkCol


class Kinase_results(Table):
    """create Kinase results table format"""
    kin_accession = Col('Accession no')
    kin_short_name = Col('Short name')
    kin_full_name = Col('Full name')
    kin_gene = Col('Gene')
    kin_organism = Col('Species')
    kin_cellular_location = Col('Cellular location')
    kin_family = Col('Family')
    detail = LinkCol('Detail', 'browse.browse_detail',
                         url_kwargs=dict(text='kin_accession'))

class Substrate_results(Table):
    """create Substrates results table format"""
    subs_accession = Col('Accession no')
    subs_short_name = Col('Short name')
    subs_full_name = Col('Full name')
    subs_protein_type = Col('Protein type')
    subs_molec_weight_kd = Col('Molecular weight (kd)')
    subs_gene = Col('Gene')
    subs_chrom_location = Col('Chromosome location')
    subs_organism = Col('Species')
    detail = LinkCol('Detail', 'browse.detail',
                         url_kwargs=dict(text='sub_accession'))