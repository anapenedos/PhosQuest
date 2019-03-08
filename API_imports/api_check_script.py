from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from data_import_scripts.api_import import get_uniprot_api_data, \
    get_pubchem_api_data, get_table_values_for_search
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base, Kinase, \
    Substrate, Inhibitor

subs_uniprot_df = get_uniprot_api_data(Substrate)
