# standard imports
import os

# project imports
from PhosphoQuest_app.service_scripts.user_data_crunch \
    import user_data_check
from PhosphoQuest_app.service_scripts.userdata_display import run_all
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.service_scripts.ud_db_queries import link_ud_to_db


s = create_sqlsession()

ad = run_all(user_data_check(os.path.join('PhosphoQuest_app',
                                          'user_data',
                                          'az20.tsv')))

sty = ad['sty']
styno = ad['styno']

dict = link_ud_to_db(styno)
