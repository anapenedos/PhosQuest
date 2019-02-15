### Python script add a column from one dataframe to another

### Import relevant modules
import pandas as pd

df1 = pd.read_csv('user_usage.csv')
df2 = pd.read_csv('user_device.csv')

newdf = pd.merge(df1,
		df2[['PubChemID', 'platform', 'device']],
		on='PubChemID')

newdf.to_csv('merge.csv')





