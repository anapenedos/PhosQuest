### Plotting Documentation

This plotting documentation outlines the methods used to analyse user input data as default once uploaded via the "User data analysis" tab on the main website. 

The plotting functionality utilizes a number of python modules. The pandas module was utilized to allow handling of data structures. Plotly and a number of related modules and libraries were utilized to generate volcano plots and pie-charts. Matplotlib was also utilized to help plot the most active kinase list. The script also utilizes some generic imports such as the session module from flask and the timeframe module from timeframe which are utilized within the script. 

The script has some generic code such as:- 

**Userfilename** - Function to create userdata_temp user id and store in session cookie.

**Read_html_to_variable** - Function to open savedfile and read lines into variable.

In terms of plotting methods, we perform a total of six analyses and output:-

i) **Summary Charts - Pie-charts**

The pie-chart function summarises various metrics and distributions within the user data. 

% Enrichment efficieny - displays the percentage of phosphorylated and unphosphorylated sites within the user data.

% of multiply-phosphorylated residues - displays the percentage of residues that are phosphorylated one or up to five times.

% Residue phosphorylation - displays the distribution of serine, threonine and tyrosine phosphorylation

The pie-chart function creates pie-charts with the following parameters:-

- A dataframe
- A header denoting the column which is to be analyzed
- A name for the output 
- Whether any row is to be removed

The pie-chart code involves two steps. Initially the row headings of the dataframe are imported as bjects and stored as a series. Specific values are then imported as a list. Any data not intended to be included in the analysis will be removed at this point. 

The layout of the pie-chart is defined along with the parameters of colour, line width and size. 

 The plot function is called and the data is generated as an image which can be saved within the html file.  

ii) **`user_data_volcano_plot()`**:
* <b>Input</b>: full phospho-sites dataframe of <b>`table_sort_parse()` function. See: [user data analysis document](documentation/user_data_analysis.md)
* Subset of the of the input dataframe, corresponding to phosphosites detected in both conditions, is passed to new variable.
* Log2 fold changes and -log10(corrected p-values) of this dataframe is then passed to the <b>`plotly`</b> function <b>`scatter()`</b>.
* Dimensions as follows: x-axis as the log2 fold change and the y-axis as the -log10(corrected p-value). 
* CSS styling and interactivity options passed to the scatter object.
* <b>Output</b>: html.


iii) **`style_df()`**:
* <b>Input</b>: 
<br><b>1</b>: significant phospho-site hits dataframe of <b>`table_sort_parse()`</b> function. See: [user data analysis document](documentation/user_data_analysis.md)
<br><b>2</b>: kinase activities dataframe of <b>`kinase_analysis()`</b> function. See: [user data analysis document](documentation/user_data_analysis.md)
* Subset of the significant phospho-site hits dataframe, corresponding to the following columns, is passed to a new variable.
* Kinase activities dataframe not processed further.
* CSS styles and auxiliary functions for passing extra styling to the table are defined.
* Dataframes, CSS styling and auxiliary functions passed into the <b>`Pandas`</b> function <b>`style`</b>.
* Over-layed heat-map applied to intensity columns (significant hits table)
* Over-layed barplots applied to log2 fold change and kinase activity columns of significant phospho-site hits and kinase activity dataframes respectively.
* <b>Output</b>: styled html tables.

iv) **Kinase & Substrate Frequencies**

The visualisations here correspond to analysis of the full list of phosphorylated-sites in the uploaded user data. Utilizing information from the database, we generate WordClouds paired with frequency charts. 

The wordcloud_freq_charts functions requires word strings and frequencies to create wordclouds and plot frequency charts for kinase and substrate sites:-

kin_word_str - string of multiple kinases
subs_sites_word_str - string of multiple subs_sites
param kinase_freq - int
kinase_target_freq - int

The return is a string variables of filenames
    
v) **Kinase activities**

The kinase activities tab allows us to query the database and cross-reference to user data. This allows us to collate all kinases that match to particular substrate/site(s). Since we know that the log2 fold changes (Treatment/Condition over Control) serve as a proxy of kinase activity, we can amalgamate these values to generate a measure of relative kinase activity.

The table generated in this tab utilizes the styled table format, with super-imposed barplots implemented. We also apply sorting to the table based on the values in the last column. In addition, if substrate/sites in your data don't match to kinases in the database, no table will be displayed.

vi) **Download data** 

This tab allows users to download the analysed data as a csv file.

