### Python script add a column from one dataframe to another

### Import relevant modules
import pandas as pd

from data_import_scripts.db_parsing import bindingDB_human, mrc_inhib_source

#df1 = pd.read_csv('Test_Inhibitors_MRC.csv')
#df2 = pd.read_csv('Test_Inhibitors_BindingDB.csv')

newdf = pd.merge(mrc_inhib_source,
	    bindingDB_human[['PubChem_CID', 'UniProt_(SwissProt)_Primary_ID_of_Target_Chain']],
		left_on='PubChem CID', right_on='PubChem_CID')

#newdf.to_csv('test.csv')




