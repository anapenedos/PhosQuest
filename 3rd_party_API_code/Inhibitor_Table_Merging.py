### Python script add a column from one dataframe to another

### Import relevant modules
import pandas as pd

from data_import_scripts.db_parsing import bindingDB_human, mrc_inhib_source

#df1 = pd.read_csv('Test_Inhibitors_MRC.csv')
#df2 = pd.read_csv('Test_Inhibitors_BindingDB.csv')

newdf = mrc_inhib_source.join(bindingDB_human, on=['PubChem CID', 'PubChem_CID'], how='left')

#newdf.to_csv('test.csv')





