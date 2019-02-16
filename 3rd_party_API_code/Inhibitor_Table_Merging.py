### Python script add a column from one dataframe to another

### Import relevant modules
import pandas as pd

df1 = pd.read_csv('Test_Inhibitors_MRC.csv')
df2 = pd.read_csv('Test_Inhibitors_BindingDB.csv')

newdf = pd.merge(df1,
		df2[['PubChem CID', 'UniProt (SwissProt) Primary ID of Target Chain']],
		on='PubChem CID')

newdf.to_csv('test.csv')





