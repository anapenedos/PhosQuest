### User data analysis script. 
### Alex and Carmen "data_crunch_fu" in action.

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
import pandas.api.types as ptypes
import numpy as np
import seaborn as sb
import matplotlib as mpl
from statsmodels.stats.multitest import fdrcorrection
from plotly.offline import init_notebook_mode,  plot
import plotly.graph_objs as go
init_notebook_mode()
import os

# --------------------------------------------------------------------------- #

### Function to read user data, check for errors and pass.
def user_data_check(data_file):
    """ 
    1 - Check user data file, and if necessary coerce to correct format. 
    2 - Check for fold calculation errors, and if correct, return data frame 
        for passing to later functions. 
    3 - If incorrect fold calculations detected, error message returned. """
    # Read user_data and assign to dataframe variable.
    orig_file = pd.read_table(data_file)
    
    # Subset source df by the first 7 columns.
    # Note: last index should be +1 bigger than number of fields.
    # AZ20.tsv file has 86 total columns, 80 of which are empty cells.
    # Necessary step to maintain indexing references at a later stage!
    orig_file_subset = orig_file.iloc[:, 0:7]
    
    # Coerce column 1 to object.
    orig_file_subset.iloc[:, 0] = orig_file_subset.iloc[:, 0].astype(object)
    
    # Coerce column 2-7 to float.
    orig_file_subset.iloc[:, 1:7] = orig_file_subset.iloc[:, 1:7].astype(float)
    
    # Subset data frame by checking if mean intensities in both columns,
    # are greater than zero.
    orig_file_subset = orig_file_subset[(orig_file_subset.iloc[:, 1] > 0) |\
                                        (orig_file_subset.iloc[:, 2] > 0)]
    
    # A data file that has been edited such that columns have been deleted,
    # i.e. in excel, may introduce "phantom" columns in python environment.
    # Such columns are coerced to "un-named" fields with nan entries.
    # If cv columns present with values, original data frame unaffected.
    # Code drops columns that contain all nan in columns.
    orig_file_subset = orig_file_subset.dropna(axis=1,    # Iterate by columns.
                                               how="all") # Drop if all na
                                                          # in columns.
                                                          
    # Determine number of columns.
    num_col = orig_file_subset.shape[1]
    
    # Check if number of cols = 5 and append new columns with "empty" entries
    # for cv calculations that are missing.
    # If number of columns adhere to correct format, data frame unaffected.
    if num_col == 5:
        orig_file_subset["control_cv"] = 1
        orig_file_subset["condition_cv"] = 1        
    
    # Add fold calculation column to df.
    orig_file_subset["calc_fold_change"] = \
        orig_file_subset.iloc[:, 2].divide(orig_file_subset.iloc[:,1])
    
    # Define user and script calculated fold changes as series variables.
    user_fold_calc = orig_file_subset.iloc[:, 3]
    script_fold_calc = orig_file_subset.iloc[:, 7]
    
    # Determine if fold change calculations match by 
    # an absolute tolerance of 3 signifcant figures.
    # Numpy "isclose()" function used to check closeness of match.
    # Boolean series returned to new column in data frame.
    orig_file_subset["check_fold_match"] = \
        np.isclose(user_fold_calc, script_fold_calc, atol=10**3)
    
    # Determine number of true matches for fold change calculations.
    # Summing of boolean series carried out: True = 1, False = 0.
    sum_matches = sum(orig_file_subset.iloc[:, 8] == 1)
    
    # Define error message if fold calculation matching determines
    # existance of errors.
    error_message = \
    ("Your incorrect fold change calculations shall not avail you..." +
     "scourge of webapps!" +
     " Your data frame SHALL NOT PASS!")
    #"Anomaly detected..PhosphoQuest will self-destruct in T minus 10 seconds")
    
    # If "sum_matches" equal to length of data frame, then reurn data frame.
    # If not, then return error message.
    if sum_matches == len(orig_file_subset):
        orig_file_parsed = orig_file_subset.iloc[:, 0:7]
        return orig_file_parsed
    elif sum_matches != len(orig_file_subset):
        return error_message

# --------------------------------------------------------------------------- #

### Function to read user data and sequentially generate data frames.
def create_filtered_dfs(parsed_data):
    """ Create data frame subsets of user data and expand
    with further analysis. """
    # Rename "Substrate" column to "Substrate (gene name)".
    parsed_data.rename(columns={parsed_data.columns[0]: \
                                "Substrate (gene name)"}, 
                                inplace=True)

    # Pass "parsed_data" to variable fed into later code.
    # Variable consists of all peptides with at least 1 quantitation.
    ud_df1_quant = parsed_data

    # Copy phospho-site id from "Substrate" field and append to new column.
    ud_df1_quant["Phospho site ID"] = ud_df1_quant.iloc[:, 0].\
                            str.extract(r"\((.*?)\)", expand=False)

    # Remove Phospho-site ID including () from "Substrate" column
    ud_df1_quant.iloc[:, 0] = ud_df1_quant.iloc[:, 0].\
                            str.replace(r"\(.*\)", "")
    
    # Parse data that contains Ser, Thr & Tyr phospho-sites only (STY)
    ud_df1_sty = ud_df1_quant[ud_df1_quant.iloc[:, 7].
                              str.contains("S|T|Y", case=False)]

    # Parse data for phospo-sites with valid p-values.
    ud_df1_sty_valid = ud_df1_sty[(ud_df1_sty.iloc[:, 4] > 0)]

    # Find max values of control vs input protein means, column header names
    cond_1_name = ud_df1_sty_valid.columns[1]
    cond_2_name = ud_df1_sty_valid.columns[2]
    # Find max of row for the 2 conditions (axis = 1 - by rows)
    condition_max = ud_df1_sty_valid[[cond_1_name, cond_2_name]].max(axis=1)

    # Calculate "fold conditions over max" values and append to new columns.
    # "df.divide" used to divide individual elements in a column by a variable.
    ud_df1_sty_valid["Fold control intensity over maximum"] =\
                    ud_df1_sty_valid.iloc[:, 1].divide(condition_max, axis=0)
    ud_df1_sty_valid["Fold condition intensity over maximum"] =\
                    ud_df1_sty_valid.iloc[:, 2].divide(condition_max, axis=0)

    # Take log10 of control & condition intensities and pass to new columns.
    ud_df1_sty_valid["Log10 control intensity"] =\
                    np.log10(ud_df1_sty_valid.iloc[:, 1])
    ud_df1_sty_valid["Log10 condition intensity"] =\
                    np.log10(ud_df1_sty_valid.iloc[:, 2])

    # Calc log2 fold change - condition/control and append as new column to df.
    ud_df1_sty_valid["Log2 fold change - condition over control"] =\
                    np.log2(ud_df1_sty_valid.iloc[:, 3])

    # Phospho-sites detected in single conditions and append to new columns.
    # Boolean true/false outputs returned.
    ud_df1_sty_valid["control only"] = ((ud_df1_sty_valid.iloc[:, 1]>0) &
                    (ud_df1_sty_valid.iloc[:, 2]==0)) # control only.
    ud_df1_sty_valid["condition only"] = ((ud_df1_sty_valid.iloc[:, 1]==0) &
                    (ud_df1_sty_valid.iloc[:, 2]>0)) # AZ20 only.

    # Phospho-sites detected in both conditions and append to new column.
    # Boolean true/false outputs returned.
    ud_df1_sty_valid["both conditions"] = ((ud_df1_sty_valid.iloc[:, 1]>0) &
                    (ud_df1_sty_valid.iloc[:, 2]>0))

    # Check if cv <=25% in both conditions.
    # Boolean true/false outputs returned.
    # Append category to new column.
    ud_df1_sty_valid["CV <=25%(both)"] = ((ud_df1_sty_valid.iloc[:, 5]<=0.25) &
                    (ud_df1_sty_valid.iloc[:, 6]<=0.25))
    
    # Check if unique sites have CVs <=25%.
    # Boolean true/false outputs returned.
    # Append category to new column.
    ud_df1_sty_valid["CV <=25%(control)"] = ((ud_df1_sty_valid.iloc[:, 5]\
                     <=0.25) & (ud_df1_sty_valid.iloc[:, 13]==1))
    ud_df1_sty_valid["CV <=25%(condition)"] = ((ud_df1_sty_valid.iloc[:, 6]\
                     <=0.25) & (ud_df1_sty_valid.iloc[:, 14]==1))
    
    return(ud_df1_quant, ud_df1_sty_valid)

# --------------------------------------------------------------------------- #

### Function to correct p-values for multiple-testing errors.
def correct_pvalue(filtered_df):
    """ Correct p-value for multiple testing errors:
    - Pass p-value series to "fdrcorrection" function of "statsmdodels" module.
    - Benjamini/Hochberg correction method used.
    - "rej_hyp" = array of rejected null hypotheses as list of boolean values.
    - "corr_p_value" = array of corrected p-values in original series order."""
    # Pass data-frame to "fdrcorrection" function.
    rej_hyp, corr_p_val = fdrcorrection(filtered_df.iloc[:, 4],
                                        alpha=0.05) # permissable error rate.

    # Convert "rej_hyp" & "corr_p_value" to data-frames.
    rej_hyp_df = pd.DataFrame(rej_hyp)
    corr_p_val_df = pd.DataFrame(corr_p_val)

    # Take -log10 of the corrected p-value.
    neg_log10_corr_p_val = (np.log10(corr_p_val_df)) * -1

    # Append "rej_hyp", "corr_p_val" &
    # "neg_log10_corr_p_val" values to new column.
    filtered_df["corrected p-value"] = corr_p_val_df.values
    filtered_df["rejected hypotheses"] = rej_hyp_df.values

    # Sort data frame by ascending p-values i.e. smallest to largest.
    filtered_df = filtered_df.sort_values(filtered_df.columns[4])

    # Sort -log10(p-values) in descending order i.e. smallest p-values
    # will have largest log10 values.
    neg_log10_corr_p_val = neg_log10_corr_p_val.sort_values(0, ascending=False)

    # Append -log10(p-values) to new column in data frame.
    # Note: "df.assign" function used for appending new column!
    # Standard column append method re-orders values and leads
    # to mis-match of p-values.
    filtered_df = filtered_df.assign(neg_log10_corr_p_values=
                                     neg_log10_corr_p_val.values)

    return(filtered_df)

# --------------------------------------------------------------------------- #

### Function to sort and parse phospho only data frame.
def table_sort_parse(filtered_df):
    """ Sort table, parse most significant hits and export to csv. """
    # Specify a new list of ordered column indices.
    # Note: not dependent on column names!
    new_col_order = [0, 7, 1, 2, 8, 9, 10, 11, 3, 12, 5, 6,
                     4, 19, 21, 20, 13, 14, 15, 16, 17, 18]

    # List comprehension to re-order df columns by new index list.
    filtered_df = filtered_df[[filtered_df.columns[i] for i in new_col_order]]

    # Sort level variables for sorting data frame.
    sort_level_1 = filtered_df.columns[15] # Rejected hypotheses.
    sort_level_2 = filtered_df.columns[21] # CV <= 0.25 in control
    sort_level_3 = filtered_df.columns[19] # CV <= 0.25 in both.
    sort_level_4 = filtered_df.columns[20] # CV <= 0.25 in condition
    sort_level_5 = filtered_df.columns[9]  # Log2 fold change.

    # Boolean sorting - true hits at top.
    filtered_df = filtered_df.sort_values(by=[sort_level_1,
                                              sort_level_2,
                                              sort_level_3,
                                              sort_level_4,
                                              sort_level_5],
                                              ascending=False)
    
    # Sum control_cv & condition cv. 
    # User data that didn't contain cv columns upon original upload,
    # would return a sum of cv's equal to length of data frame.
    # This will distinguish it from user_data with CV columns present,
    # whose sum will always be unequal to length of data frame.
    sum_cont_cv = filtered_df.iloc[:, 10].sum()
    
    # Parse phospho-sites with corrected p-values <=0.05 & CV <=25% in both 
    # conditions or CV <=25% in either control or condition.
    # Parsed table passed to new data frame.
    # Note: if original user data upload didn't contain CV's then and alternate,
    # and simplified parsing rule used.
    if sum_cont_cv == len(filtered_df):
        filtered_signif_df = filtered_df.loc[filtered_df.iloc[:, 15]]
    else:
        filtered_signif_df = filtered_df.loc[filtered_df.iloc[:, 15] &
                                             filtered_df.iloc[:, 19] |
                                             filtered_df.iloc[:, 20] |
                                             filtered_df.iloc[:, 21]]
    
    # Replace "inf" & "-inf" values in log2 fold change column with nan.
    filtered_signif_df["Log2 fold change - condition over control"]\
                      .replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Replace nan with 0.
    filtered_signif_df["Log2 fold change - condition over control"] =\
    filtered_signif_df.iloc[:, 9].fillna(0)

    return(filtered_df, filtered_signif_df)

# --------------------------------------------------------------------------- #

### Function to extract and collate info from phospho data frame.
def data_extract(filtered_df, styno):
    """ Extract data groups as follows:
        1 - Proportion of phospho-sites in total data & % enrichment.
        2 - Frequency of phosphorylated residues.
        3 - Frequency of single & multiple phosphorylations.
        4 - Total number of proteins represented. """
    ### Data group - 1.
    # Number of phospho-sites.
    phos_site_num = len(filtered_df)

    # Number of non-phosporylated peptides.
    non_phos_num = len(styno) - phos_site_num

    # Calculate % proportion of phospho-sites in total data-set.
    phos_perc_enrich = round((phos_site_num/(non_phos_num+phos_site_num)\
                              *100),1)

    # Create dictionary of variables.
    enrich_data_dict = {"Number of phospho sites": phos_site_num,
                        "Number of non-phospho sites": non_phos_num,
                        "% Enrichment": phos_perc_enrich}
    
    # Pass dictionary to dataframe object.
    data_group_1 = pd.DataFrame.from_dict(enrich_data_dict, 
                                          orient='index') # Keys as rows.
    
     # Name column for numerical data.
    data_group_1.columns = ["Total"]

    # ----------------------------------------------------------------------- #

    ### Data group - 2.
    # Calculate frequency of each phospho AA residue - case insensitive.
    phos_ser = sum(filtered_df.iloc[:, 1].str.contains("S", case=False)) # Ser.
    phos_thr = sum(filtered_df.iloc[:, 1].str.contains("T", case=False)) # Thr.
    phos_tyr = sum(filtered_df.iloc[:, 1].str.contains("Y", case=False)) # Tyr.

    # Create dictionary of variables.
    AA_data_dict = {"Serine": phos_ser,
                    "Threonine": phos_thr,
                    "Tyrosine": phos_tyr}
    
    # Pass dictionary to dataframe object.
    data_group_2 = pd.DataFrame.from_dict(AA_data_dict, 
                                          orient='index') # Keys as rows.
    
    # Name column for numerical data.
    data_group_2.columns = ["Total number with phospho"]
    
    # ----------------------------------------------------------------------- #

    ### Data group - 3.
    # Count frequency of multiply phosphorylated residues in either condition.
    # Note: duplicate intensities for the same substrate denotes that the same
    # peptide has multiple phospho-residues.
    # Counting the frequency of duplicates, therefore represents the
    # distribution of multiply-phosphorylated residues.
    # Create data frame with 3 fields from main data frame.
    df_subset = filtered_df[[filtered_df.columns[0],  # Substrate.
                             filtered_df.columns[2],  # control_mean.
                             filtered_df.columns[3]]] # AZ20_mean.

    # Parse hits unique to control & condition.
    cont_unique = df_subset.loc[(df_subset.iloc[:, 1]>0) &
                                (df_subset.iloc[:, 2]==0)]
    cond_unique = df_subset.loc[(df_subset.iloc[:, 2]>0) &
                                (df_subset.iloc[:, 1]==0)]

    # Parse hits with all intensities reported in both conditions.
    complete = df_subset.loc[(df_subset.iloc[:, 1]>0) &
                             (df_subset.iloc[:, 2]>0)]

    # "df.groupby" function used to return groups of a series.
    # Note: function iterates through data frame indices (default = by rows).
    # In this case the series is a list of intensities,
    # which is grouped by duplicates.
    # "groupby.size" function computes group sizes
    # i.e. frequency of each duplicate group.
    cont_unique_grps = cont_unique.groupby([cont_unique.iloc[:, 0],
                                            cont_unique.iloc[:, 1]]).size()

    cond_unique_grps = cond_unique.groupby([cond_unique.iloc[:, 0],
                                            cond_unique.iloc[:, 2]]).size()

    complete_grps = complete.groupby([complete.iloc[:, 0],
                                      complete.iloc[:, 1],
                                      complete.iloc[:, 2]]).size()

    # Compute summary of AA phos residue frequencies for
    # both unique control/condition & complete groups.
    cont_unique_res_freq = cont_unique_grps.value_counts()
    cond_unique_res_freq = cond_unique_grps.value_counts()
    complete_res_freq = complete_grps.value_counts()

    # Concatenate frequency series for each category.
    total_res_freq_df = pd.concat([cont_unique_res_freq,
                                   cond_unique_res_freq,
                                   complete_res_freq],
                                   axis=1) # sets join columns by rows.

    # Sum all frequency series to compute total multiply phosphorylated AA.
    total_res_freq_summary = total_res_freq_df.sum(axis=1)

    # Add categories to table.
    data_group_3 = pd.DataFrame({"Number of phosphos": range(1, 6),
                                 "Frequency": total_res_freq_summary.loc[1:6]})
    
    # ----------------------------------------------------------------------- #

    ### Data group - 4.
    # Total number of proteins represented in the phospho only data.
    num_prot_freq = df_subset.groupby([df_subset.iloc[:, 0]]).size()
    data_group_4 = len(num_prot_freq)

    # ----------------------------------------------------------------------- #

    return(data_group_1, data_group_2, data_group_3, data_group_4)

# --------------------------------------------------------------------------- #

### Function to plot heatmap of intensity data.
def heat_map(phospho_df,prefix):
    """ Apply heatmap to subset of phospho hits dataframe & export as png. """
    # Combine substrate, Phospho site ID with condition fold over max columns.
    phospho_df = phospho_df[[phospho_df.columns[0],  # Substrate.
                             phospho_df.columns[1],  # Phospho_site_ID.
                             phospho_df.columns[4],  # Fold_cont_over_max.
                             phospho_df.columns[5]]] # Fold_cond_over_max.

    # Concatenate "Substrate" & "Phospho site ID" into one string,
    # and append to new column.
    phospho_df["Phospho_site_ID"] = phospho_df.iloc[:, 0].astype(str)+"_"+\
                                    phospho_df.iloc[:, 1]

    # Parse concatenated id and fold over max columns.
    phospho_df = phospho_df[[phospho_df.columns[4],
                             phospho_df.columns[2],
                             phospho_df.columns[3]]]

    # Set "Phospho site ID" as index.
    phospho_df = phospho_df.set_index(phospho_df.iloc[:, 0].values)

    # Parse fold over max columns.
    phospho_df = phospho_df[[phospho_df.columns[1],
                             phospho_df.columns[2]]]

    # Set parameters for heatmap plot.
    phospho_fig = mpl.pyplot.figure(figsize=(16,48))
    phospho_fig.subplots_adjust(right=0.4)
    sb.heatmap(phospho_df, cmap="YlGnBu", cbar_kws={"shrink":0.25})


    file = os.path.join("kinase_db_app/static", f"{prefix}_heatmap.png")
    phospho_heatmap = phospho_fig.savefig(file)

    return (phospho_heatmap)

# --------------------------------------------------------------------------- #

### Function to style table of significant phospho sites and render to html.
def style_df(phospho_df):
    """ Apply pandas "df.style" methods to subset of phospho hits dataframe 
    and render/export as html. """
    # Parse subset of significant phospho hits.
    phospho_df = phospho_df[[phospho_df.columns[0],   # Substrate.
                             phospho_df.columns[1],   # Phospho_site_ID.
                             phospho_df.columns[4],   # Fold_cont_over_max.
                             phospho_df.columns[5],   # Fold_cond_over_max.
                             phospho_df.columns[9],   # Log2 fold change.
                             phospho_df.columns[13]]] # Corrected p-value.
    
    # Insert new column at index 0 to specify row position as integer. 
    idx = 0 # Set index for inserting column.
    idx_col = range(1, (len(phospho_df)+1)) # Specify range as 1:len(df)+1
    phospho_df.insert(loc=idx, column="Number", value=idx_col) # Insert.
    
    # Set CSS properties for pandas.style object.
    # CSS properties for table header/index in dataframe.
    th_props = [
      ('font-size', '16px'),
      ('font-family', 'Calibri'),
      ('text-align', 'center'),
      ('font-weight', 'bold'),
      ('color', '#000000'),
      ('background-color', '#708090'),
      ('border', '1px solid black'),
      ('height', '50px'),
      ('position', 'sticky'),
      ('position', '-webkit-sticky'),
      ('top', '50px'),
      ('z-index', '999'),
      ('padding', '5px'),
      ('background-clip', 'padding-box') # Required for firefox rendering of 
                                         # of borders on table headers. Header
                                         # background obscures bordering, hence
                                         # application of clipping.
      ]
    
    # CSS properties for table data in dataframe.
    td_props = [
      ('font-size', '12px'),
      ('border', '1px solid black'),
      ('text-align', 'center'),
      ('font-weight', 'bold'),
      ('background-clip', 'border-box') # Required for chrome to counter border
                                        # clipping applied to table headers.
      ]
    
    # Set table styles.
    styles = [
      dict(selector="th", props=th_props),
      dict(selector="td", props=td_props)
      ]
    
    # ----------------------------------------------------------------------- # 
    
    ### Sub-functions to ascertain unique phospho-hits, 
    ### and differentially colour and coerce log2 fold change columns.

    def colour_cond_uniques(phospho_df):
        """ Function to block fill with green, Log2 fold column cells that
        correspond to unique hits in control. """
        # Define colour for filling cells.
        col1 = "background-color: #5fba7d"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria. 
        mask = phospho_df["Fold control intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by boolean array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
    
    def colour_cont_uniques(phospho_df):
        """ Function to block fill with red, Log2 fold column cells that
        correspond to unique hits in condition. """
        # Define colour for filling cells.
        col1 = "background-color: #d65f5f"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria.
        mask = phospho_df["Fold condition intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by boolean array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
    
    def hide_zero_condition(phospho_df):
        """ Function to hide zero value in log2 fold column for
        condition only hits. """
        # Define colour of printed values.
        col1 = "color: #d65f5f"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria.
        mask = phospho_df["Fold condition intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by boolean array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
    
    def hide_zero_control(phospho_df):
        """ Function to hide zero value in log2 fold column for
        control only hits. """
        # Define colour of printed values.
        col1 = "color: #5fba7d"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria.
        mask = phospho_df["Fold control intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by booelan array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
        
    # ----------------------------------------------------------------------- # 
    # Pass data frame fields to multiple style methods.
    styled_phospho_df = (phospho_df.style
      # Use "background_gradient" method to apply heatmap to table
      # fold control & condition intensity over max values.                    
      .background_gradient(subset=["Fold control intensity over maximum", 
                                   "Fold condition intensity over maximum"], 
                           cmap="YlGnBu",   # Choose colour-map.
                           low=0, high=0.5) # Set color range .
                                            # Set "high" arg to low value. 
                                            # Accentuates differences between
                                            # low and high intensity values.
      
      # Use "bar" method to apply bar-chart styling to log2 fold change field.
      .bar(subset=["Log2 fold change - condition over control"], 
           align='mid',                  # Align bars with cells
           color=['#d65f5f', '#5fba7d']) # Bar color as 2 value/string tuple.
      
      # Set float precision for data - 2 significant figures. 
      .set_precision(2)
      
       # Pass CSS styling to styled table.
      .set_table_styles(styles)
      
      # Colour cells with 0 in control log2 fold column as green,
      # or red if cells with 0 in condition log2 fold column.
      .apply(colour_cond_uniques, axis=None)
      .apply(colour_cont_uniques, axis=None)
      .apply(hide_zero_condition, axis=None)
      .apply(hide_zero_control, axis=None))

    # Render table as html and export to wkdir.
    html = styled_phospho_df.hide_index().render()
    #with open("style_df_rename.html","w") as fp:
        #fp.write(html)

    return html

# --------------------------------------------------------------------------- #

### Function to generate volcano plot from user data.
def user_data_volcano_plot(phos_table):
    """ Function to create volcano plot of signifcantly differentially 
    expressed phosho-sites from user uploaded data """
    # Parse subset of phospho-sites table.
    vp_df_subset = phos_table[[phos_table.columns[0],   # Substrate.
                               phos_table.columns[1],   # site.
                               phos_table.columns[2],   # control mean.
                               phos_table.columns[3],   # condition mean.
                               phos_table.columns[9],   # Log2 fold change.
                               phos_table.columns[14]]] # -log10(p-value).
    
    # Concatenate "substrate" and "site" fields as single string.
    vp_df_subset["Sub_site_ID"] = vp_df_subset.iloc[:, 0].astype(str)+"_"+\
                                                    vp_df_subset.iloc[:, 1] 
                                              
    # Parse substrate_sitID, log2 fold change and p-value only.                          
    vp_df_subset = vp_df_subset[[ vp_df_subset.columns[6],  # subs_site id.
                                  vp_df_subset.columns[2],  # control mean .
                                  vp_df_subset.columns[3],  # condition mean.
                                  vp_df_subset.columns[4],  # log2 fold change.
                                  vp_df_subset.columns[5]]] # -log10(p-value)
    
    # Parse hits with intensity in both conditions.
    # Necessary as fold changes for single condition hits are "inf or -inf".
    # x-axis range, for log2 fold changes in volcano plot, 
    # cannot be set properly with these entries at a lter stage.
    vp_df_subset = vp_df_subset[(vp_df_subset.iloc[:, 1] > 0) &\
                                (vp_df_subset.iloc[:, 2] > 0)]
    
    # Set core plot.
    trace = go.Scattergl(
            x=vp_df_subset.iloc[:, 3],    # log2 fold change.
            y=vp_df_subset.iloc[:, 4],    # -log10(p-value).
            text=vp_df_subset.iloc[:, 0], # Set subs_id for hovering on points.
            opacity=0.9,                  # Point transparency: range = 0-1.
            mode='markers',               # Set drawing method for plot.
            marker=dict(                  # Set marker styling.
                size = 10,
                color=vp_df_subset.iloc[:, 3], # Colour set to -log10(p-value)
                colorscale='Portland',
                colorbar=dict(title='log2 fold change (color bar scale)'),
                showscale=True),             
    )
            
    # Define trace as data.        
    data = [trace]
    
    # Pass styling to wider plot.
    layout = {
            'title': 'Volcano plot - significance of differential expression',
            'font': {
                    'family': 'Droid Sans Mono',
                    'size': 15,
                    'color': '#666699'
                    },
            'height': 900,
            'width': 1100,
            'xaxis': {
                        'title': 'Log2 fold change: condition over control',
                        'ticklen': 5,
                        'gridwidth': 2
                    },
            'yaxis': {
                        'title': '-log10(corrected p-value)',
                        'ticklen': 5,
                        'gridwidth': 2
                    },
            'shapes': [
                    # Horizontal line to denote permissbale error rate.
                    # Error rate of 0.05 = ~1.3 (-log10 scale).
                     {
                        'type': 'line',
                        'x0': min(vp_df_subset.iloc[:, 3]),
                        'y0': 1.3,
                        'x1': max(vp_df_subset.iloc[:, 3]),
                        'y1': 1.3,
                        'line':{
                            'color': 'Black',
                            'width': 1.5,
                            'dash': 'dot',
                    },
                },
            ]        
    }
    
    # Define figure paramters.
    fig = {
          'data': data,
          'layout': layout,
    }
    
    # Define plot as html variable for calling at Flask level.
    html = plot(fig)
    return html

# --------------------------------------------------------------------------- #
    
# set up run if running this script only
if __name__ == "__main__":

    #set up runs for testing functions
    file = phos_sites_path = os.path.join('PhosphoQuest_app', 
                                          'user_data', 
                                          'az20.tsv')

    data_or_error = user_data_check(file)
    
    styno, sty = create_filtered_dfs(data_or_error)

    corrected_p = correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort = table_sort_parse(corrected_p)

    phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq =\
    data_extract(full_sty_sort, styno)

    heat_map(full_sty_sort,"full")

    heat_map(parsed_sty_sort,"sig")

    style_df(parsed_sty_sort)

    style_df(full_sty_sort)
    
    ud_volcano = user_data_volcano_plot(full_sty_sort)

    full_sty_sort.to_csv("../user_data/full_sorted_hits.csv")

    parsed_sty_sort.to_csv("../user_data/significant_sorted_hits.csv")
    
# --------------------------------------------------------------------------- #
#### Test code for analysing multi-drug treatments
#file = os.path.join('PhosphoQuest_app', 
#                        'user_data', 
#                        'mux.tsv')   
#
## read multi-treatment data into dataframe
#mux_df = pd.read_table(file)
## pass substrate and control columns to new dataframe
#mux_df_sub_cont_subset = mux_df.iloc[:, 0:2]
## take subset minus substrate and control columns
#mux_df_treat_subset = mux_df.drop(mux_df.columns[[0,1]], axis=1)
## define number of columns
#mux_df_num_col = mux_df_treat_subset.shape[1]
## define chunk size for splitting array
#mux_df_chunk_size = mux_df_num_col/5
## split dataframe treatment subset inot list of per treatment dataframes.
#mux_df_chunk_list = np.array_split(mux_df_treat_subset, mux_df_chunk_size, axis=1)
## merge each treatment subset with substrate & control column
#for df in mux_df_chunk_list:
#    df["substrate"] = mux_df.iloc[:, 0]
#    df["control_mean"] = mux_df.iloc[:, 1]
    
# --------------------------------------------------------------------------- #
#### Testing query/join code for db info extraction.
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker, Load, load_only
#from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base, Kinase, \
#     Substrate, Inhibitor, Phosphosite, kinases_phosphosites_table
#import os
#import pandas as pd
#
## Define path variable to the PhosphoQuest data-base.
#dbpath = os.path.join('database', 'PhosphoQuest.db')
## Define instance of engine which represents interface to the database.
#engine = create_engine(f'sqlite:///{dbpath}')
## Define session class object - ORM "handle" to the data-base.
#Session = sessionmaker()
## Connect engine to the Session object.
#Session.configure(bind=engine)
## Instantiate a Session - converse with data-base.
#s = Session()
## Create join query using ORM sqlalchemy language.
## Query 3 db class objects - "Substrate", "Phosphosite" & "Kinase".
## Join in logical succession according to schema!
## Specify subset of join tables to load.
#subs_phos_kin_query = s.query(Substrate, Phosphosite, Kinase).\
#                              join(Phosphosite).\
#                              join(kinases_phosphosites_table).\
#                              join(Kinase).\
#                              options(Load(Substrate).\
#                                      load_only("subs_gene"),
#                                      Load(Phosphosite).\
#                                      load_only("phos_modified_residue"),
#                                      Load(Kinase).\
#                                      load_only("kin_gene"))
#
## Query 2 db class objects - "Substrate" & "Phosphosite".
## Join in logical succession according to schema!
## Specify subset of join tables to load.
#subs_phos_query = s.query(Substrate, Phosphosite).\
#                              join(Phosphosite).\
#                              options(Load(Substrate).\
#                                      load_only("subs_gene"),
#                                      Load(Phosphosite).\
#                                      load_only("phos_modified_residue"))
#
## Pass ORM join-query subset to dataframe                     
#subs_phos_subset_df = pd.read_sql(subs_phos_query.\
#                                  statement,\
#                                  subs_phos_query.session.bind)
#
## Pass ORM join-query subset to dataframe                     
#subs_phos_kin_subset_df = pd.read_sql(subs_phos_kin_query.\
#                                      statement,\
#                                      subs_phos_kin_query.session.bind)
#
## Parse dataframe for only phosphosites.
## Parse sites with only phospho as modification.
## Regex - parse lines that end with "-p".
#subs_phos_subset_df = \
#        subs_phos_subset_df[subs_phos_subset_df.iloc[:, 3].str.\
#                            contains(r"-p$", regex=True)]
#
## Remove "-p" extension to entries.
#subs_phos_subset_df.iloc[:, 3] = \
#        subs_phos_subset_df.iloc[:, 3].str.replace("-p", "")
#
## Add column to full phos_sites table of concatenated substrate and site id.
#subs_phos_subset_df["phos_site_ID"] = subs_phos_subset_df.iloc[:, 1].\
#                                      astype(str)+"_"+\
#                                      subs_phos_subset_df.iloc[:, 3]
#                               
## Add column to signif phos_sites table of concatenated substrate and site id.
#full_sty_sort["phos_site_ID"] = full_sty_sort.iloc[:, 0].astype(str)+"_"+\
#                                full_sty_sort.iloc[:, 1]
#                                 
## Check if "phos_site_ID" in user data present in db.
## Boolean value returned to new column in full data-set.                                 
#full_sty_sort["Substrate & site in DB"] = full_sty_sort.iloc[:, 22].\
#                                          isin(subs_phos_subset_df.iloc[:, 4])
#                            
## Compute number of IDs that match to db.     
#ID_match_sum = sum(full_sty_sort.iloc[:, 23])