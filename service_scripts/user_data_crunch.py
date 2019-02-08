### User data analysis script. 
### Alex and Carmen "data_crunch_fu" in action.

# --------------------------------------------------------------------------- #

### Import packages into environment. 
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib as mpl
from statsmodels.stats.multitest import fdrcorrection

# --------------------------------------------------------------------------- #

### Function to read user data and sequentially generate data frames.
def create_filtered_dfs(datafile):
    """ Create data frame subsets of user data and expand
    with further analysis"""
    # Read user_data and assign to dataframe variable.
    ud_df_orig = pd.read_table(datafile)
    
    # Subset source df by the first 6 columns.
    # Note: last index should be +1 bigger than number of fields. 
    # tsv file has 86 total columns, 80 of which are empty cells.
    # Necessary step to maintain indexing references at a later stage!
    ud_df_orig = ud_df_orig.iloc[:, 0:7]
    
    # Parse data that contains at least 1 quant value in either condition and
    # pass to variable. Note: "df.iloc" function used to specify column indices
    # instead of column names. Allows for  different field names.
    ud_df1_quant = ud_df_orig[(ud_df_orig.iloc[:, 1] > 0) |\
                            (ud_df_orig.iloc[:, 2] > 0)]

    # Copy phospho-site id from "Substrate" field and append to new column.
    ud_df1_quant["Phospho site ID"] = ud_df1_quant.iloc[:, 0].\
                            str.extract(r"\((.*?)\)", expand=False)

    # Remove Phospho-site ID including () from "Substrate" column
    ud_df1_quant.iloc[:, 0] = ud_df1_quant.iloc[:, 0].\
                            str.replace(r"\(.*\)", "")

    # Parse data that contains only Ser, Thr, Tyr & non phospho-sites (STYN).
    ud_df2_styn = ud_df1_quant[ud_df1_quant.iloc[:, 7].
                            str.contains("S|T|Y|None", case=False)]
    # Search not case sensitive.
    # Parse data that contains Ser, Thr & Tyr phospho-sites only (STY)
    ud_df3_sty = ud_df2_styn[ud_df2_styn.iloc[:, 7].
                            str.contains("S|T|Y", case=False)]

    # Parse data for phospo-sites with valid p-values.
    ud_df4_sty_valid = ud_df3_sty[(ud_df3_sty.iloc[:, 4] > 0)]

    # Find max values of control vs input protein means, column header names
    cond_1_name = ud_df4_sty_valid.columns[1]
    cond_2_name = ud_df4_sty_valid.columns[2]
    # Find max of row for the 2 conditions (axis = 1 - by rows)
    condition_max = ud_df4_sty_valid[[cond_1_name, cond_2_name]].max(axis=1)

    # Calculate "fold conditions over max" values and append to new columns.
    # "df.divide" used to divide individual elements in a column by a variable.
    ud_df4_sty_valid["Fold control over max"] =\
                    ud_df4_sty_valid.iloc[:, 1].divide(condition_max, axis=0)
    ud_df4_sty_valid["Fold condition over max"] =\
                    ud_df4_sty_valid.iloc[:, 2].divide(condition_max, axis=0)
                    
    # Take log10 of control & condition intensities and pass to new columns.
    ud_df4_sty_valid["Log10 control intensity"] =\
                    np.log10(ud_df4_sty_valid.iloc[:, 1])
    ud_df4_sty_valid["Log10 condition intensity"] =\
                    np.log10(ud_df4_sty_valid.iloc[:, 2])

    # Calc log2 fold change - condition/control append as new column to df.
    ud_df4_sty_valid["Log2 fold change - condition over control"] =\
                    np.log2(ud_df4_sty_valid.iloc[:, 3])

    # Phospho-sites detected in single conditions and append to new columns.
    ud_df4_sty_valid["control only"] = ((ud_df4_sty_valid.iloc[:, 2]>0) &
                    (ud_df4_sty_valid.iloc[:, 3]==0)) # control only.
    ud_df4_sty_valid["condition only"] = ((ud_df4_sty_valid.iloc[:, 2]==0) &
                    (ud_df4_sty_valid.iloc[:, 3]>0)) # AZ20 only.
    
    # Phospho-sites detected in both conditions and append to new column.
    ud_df4_sty_valid["both conditions"] = ((ud_df4_sty_valid.iloc[:, 2]>0) &
                    (ud_df4_sty_valid.iloc[:, 3]>0))
    
    # Calculate if condtion CVs <=25% in both conditions.
    ud_df4_sty_valid["CV<=25% (both)"] = ((ud_df4_sty_valid.iloc[:, 5]<=0.25) &
                    (ud_df4_sty_valid.iloc[:, 6]<=0.25))
    
    return(ud_df2_styn, ud_df4_sty_valid)

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
    """ Sort table, parse most significant hits and export to csv """
    # Specify a new list of ordered column indices.
    # Note: not dependent on column names!
    new_col_order = [0, 7, 1, 2, 8, 9, 10, 11, 3, 12, 5, 6, 
                     4, 17, 19, 18, 13, 14, 15, 16]    
    
    # List comprehension to re-order df columns by new index list.          
    filtered_df = filtered_df[[filtered_df.columns[i] for i in new_col_order]] 
    
    # Sort level variable for sorting data frame.
    sort_level_1 = filtered_df.columns[15] # Rejected hypotheses.
    sort_level_2 = filtered_df.columns[19] # CV <= 0.25 in both.
    sort_level_3 = filtered_df.columns[16] # Sites in only control.
    sort_level_4 = filtered_df.columns[17] # Sites in only AZ20.
    sort_level_5 = filtered_df.columns[18] # Sites in both conditions.
    sort_level_6 = filtered_df.columns[9]  # Log2 fold change.
    
    # Boolean sorting - true hits at top.
    filtered_df = filtered_df.sort_values(by=[sort_level_1, 
                                              sort_level_2, 
                                              sort_level_3, 
                                              sort_level_4, 
                                              sort_level_5,
                                              sort_level_6], 
                                              ascending=False)  
    
    # Parse phospho-sites with corrected p-values <=0.05 
    # and CV <= 25% in both condtions - pass to new variable.
    filtered_signif_df = filtered_df.loc[filtered_df.iloc[:, 15] &
                                         filtered_df.iloc[:, 19]]
        
    return(filtered_df, filtered_signif_df)
    
# --------------------------------------------------------------------------- #
    
### Function to extract and collate info from phospho data frame.
def data_extract(filtered_df, styn):
    """ Extract data groups as follows:
        1 - Proportion of phospho-sites in total data & % enrichment.
        2 - Frequency of phosphorylated residues.
        3 - Frequency of single & multiple phosphorylations.
        4 - Total number of proteins represented. """
    ### Data group - 1.   
    # Number of phospho-sites. 
    phos_site_num = len(filtered_df)
    
    # Number of non-phosporylated peptides.
    non_phos_num = len(styn) - phos_site_num  
    
    # Calculate % proportion of phospho-sites in total data-set.
    phos_perc_enrich = round((phos_site_num/(non_phos_num+phos_site_num)\
                              *100),1)
    
    # Concatenate into data frame.
    data_group_1 = pd.DataFrame({"number of phospho sites": phos_site_num,
                                 "number of non-phospho sites": non_phos_num,
                                 "%_enrichment": phos_perc_enrich},
                                 index=[0])
    
    # ----------------------------------------------------------------------- #
    
    ### Data group - 2.
    # Calculate frequency of each phospho AA residue - case insensitive.
    phos_ser = sum(filtered_df.iloc[:, 1].str.contains("S", case=False)) # Ser.
    phos_thr = sum(filtered_df.iloc[:, 1].str.contains("T", case=False)) # Thr.
    phos_tyr = sum(filtered_df.iloc[:, 1].str.contains("Y", case=False)) # Tyr.
    
    # Concatenate into data frame.
    data_group_2 = pd.DataFrame({"serine": phos_ser,
                                 "threonine": phos_thr,
                                 "tyrosine": phos_tyr},
                                 index=[0])
    
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
    # both unique control/condition & complete gropus
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
def heat_map(phospho_df, filename):
    # Combine substrate, Phospho site ID with condition fold over max columns.
    phospho_df =  phospho_df[[phospho_df.columns[0],  # Substrate.
                              phospho_df.columns[1],  # Phospho_site_ID.
                              phospho_df.columns[4],  # Fold_cont_over_max.
                              phospho_df.columns[5]]] # Fold_cond_over_max.    
    
    # Concatenate "Substrate" & "Phospho site ID" into one column, 
    # and append to new column.
    phospho_df["Phospho_site_ID"] = phospho_df.iloc[:, 0].astype(str)+"_"+\
                                    phospho_df.iloc[:, 1]
    
    # Parse concatenated id and fold over max columns.
    phospho_df = phospho_df[[phospho_df.columns[1],
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
    phospho_heatmap = phospho_fig.savefig(f"{filename}_heatmap.png")
    
    return(phospho_heatmap)
    
# --------------------------------------------------------------------------- #
    
# set up run if running this script only
if __name__ == "__main__":

    #set up runs for testing functions
    file = 'AZ20.tsv'

    styn, sty = create_filtered_dfs(file)

    corrected_p = correct_pvalue(sty)
    
    full_sty_sort, parsed_sty_sort = table_sort_parse(corrected_p)
    
    data_1, data_2, data_3, data_4 = data_extract(full_sty_sort, styn)
    
    heat_map(full_sty_sort)
    
    heat_map(parsed_sty_sort)

    full_sty_sort.to_csv("../user_data/full_sorted_hits.csv")
    
    parsed_sty_sort.to_csv("../user_data/significant_sorted_hits.csv")

# --------------------------------------------------------------------------- #