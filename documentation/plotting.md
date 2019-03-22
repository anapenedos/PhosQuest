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

ii) **Volcano plot**

The volcano plot function generates a scatter plot of Log2 fold changes vs -log10(corrected p-values) from the user data uploaded. The code utilizes the following column data:-

- Substrate
- Site
- Control mean
- Condition mean
- Log2 fold change
- -log10(corrected p-value)

The volcano plot is created by initially invoking the go.Scatter function and specifically denoting the x-axis as the log2 fold change, and the y-axis as the -log10(corrected p-value). Specific parameters are set for the visualisation of the volcano plot. The plot function generates the image and this is uploaded into the respective html file.

iii) **Processed Table**

The processed table lists the substrate data provided from the user-upload file and a number of additional datasets. The table corresponds to hits, whose corrected p-values meet an error rate threshold of <=0.05 and have a CV of <=25%. If the original upload table did not include CV columns, then only the p-value threshold is applied.

- Substrate (gene name)
- Phosphosite ID
- Substrate/isoform in DB (gene name)
- Phosphosite in DB (ID)
- Kinase in DB 
- Fold control intensity over maximum
- Fold condition intensity over maximum
- Log2 fold change - condition over control 
- Corrected p-value

For the intensity columns, the original intensity values were transformed by dividing each substrate/site intensity by the maximum intensity of the row (both conditions). This scaling allowed the application of a heatmap to the cells, for visual clarification of intensity differences.

Log2 fold changes were presented as barplots and are integrated into the column, that scale with the fold change values. When cells that are fully coloured, this denotes hits detected in only one condition.

For sorting, the Log2 fold changes were used, giving a gradated ordering of hits as you scroll through the table.

The code for the processed table is split into a number of functions where some are related to the drawing of the table, and some to the calculations required for the different columns. 

**Style_df** - Function to style table of significant phospho sites and render to html.

**colour_cond_uniques** - Sub-functions to ascertain unique phospho-hits, 
    and differentially colour and coerce log2 fold change columns.
    
**styled_phospho_df** - Pass data frame fields to multiple style methods.        

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

