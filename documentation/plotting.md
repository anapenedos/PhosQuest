# <center><u>Plotting</center>

### <u>Main script</u>:  `plotting.py`

### <u>Webapp folder location</u>:  `PhosphoQuest\service_scripts`

### <u>Technologies and tools</u>:  `Python, Pandas, Plotly, Matplotlib, WordCloud, Flask`

### <u>Strategy</u>: 

This plotting documentation outlines the methods used to analyse user input data once uploaded via the "User data analysis" section on the main website. 

The plotting functionality utilizes a number of python modules. The <b>`Pandas`</b> module was utilized to allow handling of data structures. <b>`Plotly`</b> and a number of related modules and libraries were utilized to generate volcano plots and pie-charts. <b>`Matplotlib`</b> was also utilized to help plot the most active kinase list. The script also utilizes some generic imports such as the session module from flask and the timeframe module from timeframe which are utilized within the script.  

### <u>Functions</u>:

The script has some generic code such as:- 

i) **`create_userfilename()`**: Function to create userdata_temp user id and store in session cookie.

ii) **`read_html_to_variable()`**: Function to open savedfile and read lines into variable.

iii) **`pie_chart()`**: piecharts of "Metrics" data, summarising various distributions within the user data.

<b>Input</b>: dataframe outputs <b>`data_extract()`</b> function. See: [user data analysis document](documentation/user_data_analysis.md)
<br><b>1</b>: dataframe 1 - % enrichment.
<br><b>2</b>: dataframe 2 - Phosphorylated AA residue frequency distribution.
<br><b>3</b>: dataframe 3 - Multiple phosphorylation frequency distribution. 
* Generating pie-charts involves two steps. Initially the row headings of the dataframes are imported as objects and stored as a series. Specific values are then imported as a list. Any data not intended to be included in the analysis will be removed at this point. 
* The layout of the pie-chart is defined along with the parameters of colour, line width and size. 
* Variables and layout are then passed to the <b>`plotly`</b> function <b>`pie()`</b>.
<b>Output</b>: 3 interactive pie-charts as html.  

iv) **`style_df()`**: Styled tables for analysed user table and relative kinase activities.
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

v) **`user_data_volcano_plot()`**: plot for displaying distribution of significantly differentially regulated phospho-sites.
* <b>Input</b>: full phospho-sites dataframe of <b>`table_sort_parse()`</b> function. See: [user data analysis document](documentation/user_data_analysis.md)
* Subset of the of the input dataframe, corresponding to phosphosites detected in both conditions, is passed to new variable.
* Log2 fold changes and -log10(corrected p-values) of this dataframe is then passed to the <b>`plotly`</b> function <b>`scatter()`</b>.
* Dimensions as follows: x-axis as the log2 fold change and the y-axis as the -log10(corrected p-value). 
* CSS styling and interactivity options passed to the scatter object.
* <b>Output</b>: html.

vi) **`wordcloud_freq_charts()`**: Wordcloud and barplots for kinase and substrate/sites frequency analysis.

* <b>Input</b>: dataframes and wordlist outputs of <b>`kinase_analysis()`</b> function. See: [user data analysis document](documentation/user_data_analysis.md)
<br><b>1</b>: dataframe 1 - Kinase frequency distribution analysis (top 30 most active kinases).
<br><b>2</b>: dataframe 2 - Substrate/site frequency distribution analysis (top 30 most targeted substrate/sites).
<br><b>3</b>: word list 1 - kinases (top 30 most active kinases).
<br><b>4</b>: word list 2 - substrate/site (top 30 most targeted substrate/sites).
* Dataframes fed into <b>`matplotlib`</b> plotting function <b>`bar()`</b>. Barplot objects returned with various styling. 
* Word lists fed into <b>`wordcloud`</b> function <b>`WordCloud()`</b>. WordCloud objects returned with various styling.
* <b>Output</b>: pngs of wordclouds and barplots.

### <u>Further work</u>:

1. The volcano plot has the potential for a susbtantial expansion of interaction options and visuals:
* User input fields could be generated that allow the user to shift the dashed thresholds that currently hard-coded. 
* Another useful option would be to enable user selection of points, such that they are labeled for image export. An alternative approach would be to have a function that displays selected hits as a table on the webapp volcano plot tab. This has been implemented in a scatter here: <https://plot.ly/python/selection-events/>
* The volcano plot tab could also implement extra visualisation in the form of density distributions of log10 intensity data. This may inform the user as to whether the underlying assumption of t-test calculations, i.e. data is normally distributed, can be corroborated.



