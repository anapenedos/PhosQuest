### Python script add a column from one dataframe to another

### Import relevant modules
import pandas as pd

from data_import_scripts.table_parsing import bdb_inhib_import, mrc_inhib_import


# import required data frames
bindingDB_human = bdb_inhib_import()
mrc_inhib_source = mrc_inhib_import()
#df1 = pd.read_csv('Test_Inhibitors_MRC.csv')
#df2 = pd.read_csv('Test_Inhibitors_BindingDB.csv')

newdf = pd.merge(mrc_inhib_source,
	    bindingDB_human[['PubChem_CID', 'UniProt_(SwissProt)_Primary_ID_of_Target_Chain']],
		left_on='PubChem CID', right_on='PubChem_CID')

#newdf.to_csv('test.csv')





