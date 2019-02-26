### Basic data analysis on dataframes generated using crunch file

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
import os
import numpy as np
from bokeh.io import show, output_file
from bokeh.plotting import figure

# --------------------------------------------------------------------------- #

### Import the dataframes from Alex's script
# Call the specific file
file = phos_sites_path = os.path.join('user_data', 'AZ20.tsv')

# Call the specifc script from Userdata_display
from service_scripts import userdata_display

# Create the dataframe
df = userdata_display.run_all(file)

# List a number of variable calling results from Userdata_display
phos_enrich = df['datalist'][0]
AA_mod_res_freq = df['datalist'][1]
multi_phos_res_freq = df['datalist'][2]
prot_freq = df['datalist'][3]
styn = df['styn']

# --------------------------------------------------------------------------- #

### Creat a bar chart of the dataframe data
# Bar graph of AA_mod_res_freq dataframe

### As an example, the data should be placed into a series such as this
#Amino acids= ['Serine', 'Threonine', 'Tyrosine']
#Numbers = [9333, 1244, 171]

output_file("AA_mod_res_frequency.html")

# Import the row heading data e.g. Amino acids
rows1 = pd.Series(AA_mod_res_freq.index)

# Place them into a series (not as objects)
listOfRowIndexLabels1 = list(rows1)

# Import the specific values from the dataframe
columns1 = AA_mod_res_freq.values

# Place them into a series (not as objects)
listOfColumnNames1 = list(columns1)

# Create the figure with specific parameters
p = figure(x_range=listOfRowIndexLabels1, plot_height=250, title="Total number with phospho",
           toolbar_location=None, tools="")

p.vbar(x=listOfRowIndexLabels1, top=listOfColumnNames1, width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0
show(p)

# --------------------------------------------------------------------------- #

### Creat a bar chart of the dataframe data
# Bar graph of Phos_enrich

### As an example, the data should be placed into a series such as this
#Amino acids= ['Serine', 'Threonine', 'Tyrosine']
#Numbers = [9333, 1244, 171]

output_file("phos_enrich.html")

# Import the row heading data e.g. Amino acids
rows2 = pd.Series(phos_enrich.index)

# Place them into a series (not as objects)
listOfRowIndexLabels2 = list(rows2)

# Import the specific values from the dataframe
columns2 = phos_enrich.values

# Place them into a series (not as objects)
listOfColumnNames2 = list(columns2)

# Create the figure with specific parameters
p = figure(x_range=listOfRowIndexLabels2, plot_height=250, title="Total",
           toolbar_location=None, tools="")

p.vbar(x=listOfRowIndexLabels2, top=listOfColumnNames2, width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0
show(p)

# --------------------------------------------------------------------------- #

### Creat a bar chart of the dataframe data
# Bar graph of Multi_phos_res_freq

### as an example, the data should be placed into a series such as this
#Amino acids= ['Serine', 'Threonine', 'Tyrosine']
#Numbers = [9333, 1244, 171]

output_file("multi_phos_res_freq.html")

# Import the row heading data e.g. Amino acids
rows3 = pd.Series(multi_phos_res_freq.index)

# Place them into a series (not as objects)
listOfRowIndexLabels3 = list(rows3)

# Import the specific values from the dataframe
columns3 = multi_phos_res_freq["Frequency"]

##### I need to transpose this!!! ######

# Place them into a series (not as objects)
listOfColumnNames3 = list(columns3)

# Create the figure with specific parameters
p = figure(x_range=listOfRowIndexLabels3, plot_height=250, title="Frequency",
           toolbar_location=None, tools="")

p.vbar(x=listOfRowIndexLabels3, top=listOfColumnNames3, width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0
show(p)

# --------------------------------------------------------------------------