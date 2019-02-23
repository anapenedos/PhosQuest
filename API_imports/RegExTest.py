### Test area for regular expression functionality.

import pandas as pd

example = {'Subcellular location [CC]': ['SUBCELLULAR LOCATION: Mitochondrion inner membrane {ECO:0000256|RuleBase:RU000369]}']}

dftest = pd.DataFrame(example, columns = ['Subcellular location [CC]'])

#dftest['Subcellular location2'] = dftest['Subcellular location [CC]'].str.extract('([^SUBCELLULAR LOCATION: ].+[{.+])', expand=True)
dftest['Subcellular location2'] = dftest['Subcellular location [CC]'].str.extract('(?<=SUBCELLULAR LOCATION: )(.*)(?={)', expand=True)

#dftest['Subcellular location2']
