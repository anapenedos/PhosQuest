from data_import_scripts.api_import import get_uniprot_api_data, \
    get_pubchem_api_data
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Inhibitor


kin_uniprot_df = get_uniprot_api_data(Kinase)
subs_uniprot_df = get_uniprot_api_data(Substrate)
inh_pubch_df = get_pubchem_api_data(Inhibitor)
