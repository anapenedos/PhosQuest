# <center><u>User data analysis: general summary</center>

### <u>Main script</u>:  `user_data_crunch.py`

### <u>Webapp folder location</u>:  `PhosphoQuest\service_scripts`

### <u>Technologies and tools</u>:  `Python, Pandas, NumPy, statsmodels`

### <u>Strategy</u>: 

The script primarily utilises the <b>`Pandas`</b> library for data handling operations such as reading, defining and transforming data structures, filtering, subsetting, indexing, categorising, column insertion, merging of data-frames and various other tasks. <b>`Pandas`</b> is a software library written for the <b>`Python`</b> programming language and is optimised for data wrangling and analysis. 

For specific operations such as float handling and statistics operations, <b>`NumPy`</b> and <b>`statsmodels`</b> packages are also utilised.

The overall aim of the script is to perform a sequential series of operations that transform, analyse, summarise and extract user data, such that visualisation is possible at a later stage. 

These steps are handled by 6 inter-linked functions that have been divided into different data handling categories.

### <u>User data</u>:
Data takes the form of a table comprising one identifier column (mixed text & numerical fields) and six integer/float columns for a total of seven categories, with the number of records varying from 1000's to 10000's of rows. The script is written to handle a table of these dimensions, however some flexibility is afforded the user. See function: <b>`user_data_check()`</b>.   

### <u>Functions</u>:

**1. `user_data_check()`**:  <em>Data table structure check and basic filtering.</em>
* <b>Input</b>: user data table.
* Implements an error check in case of issues such as missorting of the original table. The function calculates fold changes based on intensity column inputs and then checks if the values match the original uploaded values. Boolean values returned, are used to determine if the table should be passed for later processing or return an error message.
* Determines the format of the input table by checking how many columns are present. If CV columns missing, these columns are appended with entry values of 1. Summing these "mock" CV columns gives a value equal to the length of the dataframe. This is utilised at a later stage for filtering the data. See function: <b>`table_sort_parse()`</b>.
* Parse data entries that have at least 1 quantitation value.
* <b>Output</b>: filtered dataframe or error message.

**2. `create_filtered_dfs()`**:  <em>Dataframe analysis and filtering.</em>
* <b>Input</b>: dataframe output of <b>`user_data_check()`</b> function.
* Splits ID entry into separate gene name and site columns.
* Performs a series of calculations, transformations and logical checks. This analysis is appended as extra columns in the table.
* Filters the dataframe to include only phospho-site entries.
* <b>Output</b>: 
<br><b>1</b>: analysed dataframe of phospho-hits only. 
<br><b>2</b>: dataframe of all entries.

**3. `correct_pvalue()`**:  <em>Further analysis of p-values in filtered dataframe.</em>
* <b>Input</b>: phospho-hits dataframe output of <b>`create_filtered_dfs()`</b> function.
* <b>`fdrcorrection()`</b> function of <b>statsmodels</b> is used to correct p-values for multiple-testing errors. 
* Benjamini-Hochberg method for multiple testing correction utilised.
* Permissible error rate = 0.05.
* Analysis appended to dataframe as 2 extra columns: rejected hypotheses (boolean) and corrected p-values.
* <b>Output</b>: dataframe with expanded analysis.

**4. `table_sort_parse()`**:  <em>Table sorting and filtering.</em>
* <b>Input</b>: phospho-hits dataframe output of <b>`correct_pvalue()`</b> function.
* Dataframe columns re-organised into new order for legibility.
* Sorting of dataframe using various categories calculated in preceding functions. 
* Call <b>`link_ud_to_db()`</b> function which cross-references user data with PhosphoQuest database. This analysis returns 2 dictionaries:
<br><b>1</b>: Dictionary 1 entries are appended as 3 extra columns into the main dataframe.
<br><b>2</b>: Dictionary 2 passed for further analysis. See function: <b>`kinase_analysis()`</b>.
* Differential dataframe filtering according to various categories in previous analyses. If CV columns are not present in the original uploaded data, then only the corrected p-value threshold (<=0.05) is applied. If CVs present, then both CV and corrected p-value thresholds are utilised.
* Dataframe of phospho-hits only is fed into the <b>`user_data_volcano_plot()`</b> function of the <b>`plotting.py`</b> script.
* Dataframe of significant hits is fed into the <b>`style_df()`</b> function of the <b>`plotting.py`</b> script.
* <b>Output</b>: 
<br><b>1</b>: analysed dataframe of all phospho-hits only. 
<br><b>2</b>: dataframe of significant phospho-hits.
<br><b>3</b>: kinase dictionary.

**5. `data_extract()`**:  <em>Further analysis to generate metrics of the user data.</em>
* <b>Input</b>: 
<br><b>1</b>: phospho-hits only dataframe output of <b>`table_sort_parse()`</b> function.
<br><b>2</b>: all hits dataframe output of <b>`user_data_check()`</b> function.
* 4 sets of analyses carried out to produce a "Metrics" of the data for later visualisation.
* Data is fed into the <b>`pie_chart()`</b> function of the <b>`plotting.py`</b> script.
* <b>Output</b>: 3 dataframes and 1 integer value.
<br><b>1</b>: dataframe 1 - % enrichment.
<br><b>2</b>: dataframe 2 - Phosphorylated AA residue frequency distribution.
<br><b>3</b>: dataframe 3 - Multiple phosphorylation frequency distribution.
<br><b>4</b>: integer - number proteins represented in the data.

**6. `kinase_analysis()`**:  <em>Kinase and corresponding substrate/sites analysis and kinase relative actvity calculations.</em>
* <b>Input</b>: 
<br><b>1</b>: kinase dictionary from <b>`table_sort_parse()`</b> function.
<br><b>2</b>: significant hits dataframe output of <b>`table_sort_parse()`</b> function.
* <b>Analysis 1</b> - Kinase and corresponding substrate/sites analysis:
* Kinase dictionary converted to a dataframe with each row a unique kinase (also index), with the first column a set of substrate/site(s) per kinase.
* Dataframe transformed such that each kinase has 1 unique substrate/site per row.
* Further calculation determines frequency distributions for each kinase and substrate/site. These are fed into the <b>`wordcloud_freq_charts()`</b> function of the <b>`plotting.py`</b> script.
* Lists of kinases and substrate/sites are each converted to lists of strings. These are fed into the <b>`wordcloud_freq_charts()`</b> function of the <b>`plotting.py`</b> script.
* <b>Analysis 2</b> - kinase relative activity calculation:
* Subset of significant hits dataframe generated and hits with both intensities reported are parsed.
* Dataframe generated in <b>Analysis 1</b> (converted kinase dictionary) is merged with significant hits subset, based on matching substrate/sites.
* Calculate mean of absolute log2 fold changes.
* Calculate sum of log2 fold changes and then pass sign (positive/negative) to mean of absolute log2 fold changes.
* These relative activity values are mapped to the corresponding list of substrate/site(s) as a new dataframe. This data is fed into the <b>`style_df()`</b> function of the <b>`plotting.py`</b> script.
* <b>Output</b>: 2 dataframes and 2 word lists.
<br><b>1</b>: dataframe 1 - Kinase frequency distribution analysis.
<br><b>2</b>: dataframe 2 - Substrate/site frequency distribution analysis.
<br><b>3</b>: word list 1 - kinases.
<br><b>4</b>: word list 2 - substrate/site.

### <u>Limitations and further work</u>:

1. Generally the script is somewhat flexible with regards to the user data input i.e. CV columns may or not be present and non-phosphorylated entries in the table can also be just gene-names. However, users will likely use a number of different proteomics software packages to generate their data. The raw format of these output tables will necessitate some data wrangling, pre-upload to PhosphoQuest. This increases the chances of table format issues i.e. such as missorting of columns (which the crunch script partially takes into account). Improvements in <b>`user_data_check()`</b> could assess whether: P-values are not assigned to hits with intensities reported and CVs assigned for hits with intensity of 0 reported in both replicates.
2. Code a template that takes a more raw output table from the user i.e. closer to the native analysis of proteomics software packages. Intensity columns, for example, maybe reported for the separate replicates of each experiment i.e. control and treatment/condition. The advantage of this approach, is that less needs to be done by the user and it  should decrease the likely hood of issues cropping-up such as those mentioned earlier. The disadvantage is that the burden of averaging intensities, calculating CVs and p-values will fall on the script. This will necessitate a substantial expansion of the script.
3. <b>`correct_pvalue()`</b> function could be expanded to include other methods such as the more stringent Bonferroni method. 
4. Currently there are a number of "metrics" calculated by the <b>`kinase_analysis()`</b> function, that could be used to create a small summary table to compliment the current visuals. These include measures such as the number of unique kinases that map to user data substrate/sites (and vice-versa) and the sum of kinase and substrate/site frequencies. 

