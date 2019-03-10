# standard imports
import os

from PhosphoQuest_app.service_scripts.ud_db_queries import link_ud_to_db, \
    format_db_links
from PhosphoQuest_app.service_scripts.user_data_crunch \
    import user_data_check
from PhosphoQuest_app.service_scripts.userdata_display import run_all
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from sqlalchemy.orm import Load
import pandas as pd


ad = run_all(user_data_check(os.path.join('PhosphoQuest_app',
                                          'user_data',
                                          'az20.tsv')))

sty = ad['sty']
styno = ad['styno']

sites_dict, kin_dict = link_ud_to_db(styno)

# session = create_sqlsession(session_type='pandas_sql')
# query = session.query(Substrate, Phosphosite, Kinase)\
#         .outerjoin(Phosphosite)\
#         .outerjoin(kinases_phosphosites_table)\
#         .outerjoin(Kinase)\
#         .options(Load(Substrate).load_only("subs_gene"),
#                  Load(Phosphosite).load_only("phos_modified_residue"),
#                  Load(Kinase).load_only("kin_gene"))
#subs_phos_kin_subset_df = pd.read_sql(subs_phos_kin_query.\
#                                      statement,\
#                                      subs_phos_kin_query.session.bind)