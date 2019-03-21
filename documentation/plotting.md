### Plotting Documentation

This plotting documentation outlines the methods used to analyse user input data as default once uploaded via the "User data analysis" tab on the main website. 

The plotting functionality utilizes a number of python modules. The pandas module was utilized to allow handling of data structures. Plotly and a number of related modules and libraries were utilized to generate volcano plots and pie-charts. Matplotlib was also utilized to help plot the most active kinase list. The script also utilizes some generic imports such as the session module from flask and timeframe module from timeframe which are utilized in various aspects of the script. 

The script has some generic code such as:- 

**Userfilename** - Function to create userdata_temp user id and store in session cookie

**Read_html_to_variable** - Function to open savedfile and read lines into variable

In terms of plotting functionality:-

i) **Pie-charts**

The pie-chart function creates pie-charts with the following parameters:-

- A dataframe
- A header denoting the column header which is to be analyzed
- A name for the output 
- Whether any row is to be removed

The pie-chart code involves two steps. Initially the row headings of the dataframe are imported ad objects and stored as a series. Then the specific values are imported as a list. Any data not included in the analysis will be removed at this point. 

The layout of the pie-chart is defined along with the parameters of colour, line width and size. 

 The plot function is called and the data is generated as an image which can be saved within the html file.  

Other general functions are:-       
    
**Style_df** - unction to style table of significant phospho sites and render to html.

**colour_cond_uniques** - Sub-functions to ascertain unique phospho-hits, 
    and differentially colour and coerce log2 fold change columns.
    
**styled_phospho_df** - Pass data frame fields to multiple style methods.


ii) **Volcano plots**

The volcano plot function creates a volcano plot of statistically differentially expressed phospho-sites from user uploaded data. The code utilizes the following column data:-

- Substrate
- Site
- Control mean
- Condition mean
- Log2 fold change
- -log10(p-value)

The volcano plot is created by initially invoking the go.Scatter function and specifically denoting the x-axis as the log2 fold change, and the y-axis as the -log10(p-value). Specific parameters are set for the visualisation of the volcano plot. The plot function generates the image and this is uploaded into the respective html file.




        
