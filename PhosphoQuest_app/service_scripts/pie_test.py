### Import packages into environment.
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd

 --------------------------------------------------------------------------- #
### Pie chart for phos_enrich.

# Example data
# labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
# values = [4500,2500,1053,500]

# Import the row heading data as object.
label0 = pd.Series(phos_enrich.index)
# Place them into a series (not as objects).
labels = list(label0)

# Import the specific values from the dataframe as a list.
values = phos_enrich['Total'].tolist()
values2 = values.pop(2)

# Set core pie.
trace = go.Pie(labels=labels, values=values)

# Define trace as data.
data = [trace]

# Plot the data in html format.
plot(data, filename='basicpie.html', auto_open=True)

# --------------------------------------------------------------------------- #
### Pie chart for AA_mod_res_freq.

# Example data
# labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
# values = [4500,2500,1053,500]

# Import the row heading data as object.
label0 = pd.Series(AA_mod_res_freq.index)
# Place them into a series (not as objects).
labels = list(label0)

# Import the specific values from the dataframe as a list.
values = AA_mod_res_freq['Total number with phospho'].tolist()

# Set core pie.
trace = go.Pie(labels=labels, values=values)

# Define trace as data.
data = [trace]

# Plot the data in html format.
plot(data, filename='basicpie2.html', auto_open=True)

# --------------------------------------------------------------------------- #

### Pie chart for Multi_phos_res_freq.

# Example data
# labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
# values = [4500,2500,1053,500]

# Import the row heading data as object.
label0 = pd.Series(multi_phos_res_freq.index)
# Place them into a series (not as objects).
labels = list(label0)

# Import the specific values from the dataframe as a list.
values = multi_phos_res_freq['Frequency'].tolist()

# Set core pie.
trace = go.Pie(labels=labels, values=values)

# Define trace as data.
data = [trace]

# Plot the data in html format.
plot(data, filename='basicpie3.html', auto_open=True)

# --------------------------------------------------------------------------- #
