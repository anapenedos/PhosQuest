### User data analysis script. 

# --------------------------------------------------------------------------- #

### Import packages into environment.
import os
import pandas as pd
import numpy as np
from statsmodels.stats.multitest import fdrcorrection

### Project imports
from PhosphoQuest_app.service_scripts.ud_db_queries import link_ud_to_db

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
    
    # Check if number of cols = 5 and append new columns with all entries
    #  = to 1 for cv calculations that are missing.
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
    ("Anomaly detected..PhosphoQuest will self-destruct in T minus 10 seconds"+
    "...just kidding! Please check your fold change calculations, "+
    "a discrepancy has been detected.")
    
    # If "sum_matches" equal to length of data frame, then return data frame.
    # If not, return error message.
    # Note: if first logical test passes, this indicates that fold change
    # calculations in original user data are correct (within tolerance),
    # and filtered dataframe returned for further analysis.
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
    # Df consists of all peptides with at least 1 quantitation.
    parsed_data.rename(columns={parsed_data.columns[0]: \
                                "Substrate (gene name)"}, 
                                inplace=True)

    # Copy phospho-site id from "Substrate" field and append to new column.
    parsed_data["Phospho site ID"] = parsed_data.iloc[:, 0].\
                            str.extract(r"\((.*?)\)", expand=False)

    # Remove Phospho-site ID including () from "Substrate" column
    parsed_data.iloc[:, 0] = parsed_data.iloc[:, 0].\
                            str.replace(r"\(.*\)", "")
    
    # Parse data that contains Ser, Thr & Tyr phospho-sites only (STY)
    # Note: setting na = false in contains() function allows code to deal
    # with subs_sites entries where "(None)" isn't present in the original
    # susbtrates column.
    ud_df1_sty = parsed_data[parsed_data.iloc[:, 7].
                            str.contains("S|T|Y", case=False, na=False)]

    # Parse data for phospo-sites with valid p-values.
    ud_df1_sty_valid = ud_df1_sty[(ud_df1_sty.iloc[:, 4] > 0)]

    # Find max of row for the 2 conditions (axis = 1 - by rows).
    # Note: indexer range should be last index postion +1.
    condition_max = ud_df1_sty_valid.iloc[:, 1:3].max(axis=1)

    # Calculate "fold conditions over max" values and append to new columns.
    # "df.divide" used to divide individual elements in a column by a variable.
    ud_df1_sty_valid.loc[:, "Fold control intensity over maximum"] =\
                    ud_df1_sty_valid.iloc[:, 1].divide(condition_max, axis=0)
    ud_df1_sty_valid.loc[:, "Fold condition intensity over maximum"] =\
                    ud_df1_sty_valid.iloc[:, 2].divide(condition_max, axis=0)

    # Take log10 of control & condition intensities and pass to new columns.
    ud_df1_sty_valid.loc[:, "Log10 control intensity"] =\
                    np.log10(ud_df1_sty_valid.iloc[:, 1])
    ud_df1_sty_valid.loc[:, "Log10 condition intensity"] =\
                    np.log10(ud_df1_sty_valid.iloc[:, 2])

    # Calc log2 fold change - condition/control and append as new column to df.
    ud_df1_sty_valid.loc[:,"Log2 fold change - condition over control"] =\
                    np.log2(ud_df1_sty_valid.iloc[:, 3])

    # Phospho-sites detected in single conditions and append to new columns.
    # Boolean true/false outputs returned.
    ud_df1_sty_valid.loc[:, "control only"] =\
            ((ud_df1_sty_valid.iloc[:, 1]>0) &
             (ud_df1_sty_valid.iloc[:, 2]==0)) # control only.
    ud_df1_sty_valid.loc[:, "condition only"] =\
            ((ud_df1_sty_valid.iloc[:, 1]==0)&
             (ud_df1_sty_valid.iloc[:, 2]>0)) # AZ20 only.

    # Phospho-sites detected in both conditions and append to new column.
    # Boolean true/false outputs returned.
    ud_df1_sty_valid.loc[:, "both conditions"] =\
            ((ud_df1_sty_valid.iloc[:, 1]>0) &
             (ud_df1_sty_valid.iloc[:, 2]>0))

    # Check if cv <=25% in both conditions.
    # Boolean true/false outputs returned.
    # Append category to new column.
    ud_df1_sty_valid.loc[:, "CV <=25%(both)"] =\
            ((ud_df1_sty_valid.iloc[:, 5]<=0.25) &
             (ud_df1_sty_valid.iloc[:, 6]<=0.25))
    
    # Check if unique sites have CVs <=25%.
    # Boolean true/false outputs returned.
    # Append category to new column.
    ud_df1_sty_valid.loc[:, "CV <=25%(control)"] =\
            ((ud_df1_sty_valid.iloc[:, 5]<=0.25) & 
             (ud_df1_sty_valid.iloc[:, 13]==1))
    ud_df1_sty_valid.loc[:, "CV <=25%(condition)"] =\
            ((ud_df1_sty_valid.iloc[:, 6]<=0.25) & 
             (ud_df1_sty_valid.iloc[:, 14]==1))
    
    return(parsed_data, ud_df1_sty_valid)

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

    # Variables for sorting data frame.
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
    
    # Call "link_ud_to_db" function to extract user data/db alignment data. 
    # Dictionaries returned as follows:
    # "db_ud_dict" = dictionary of 3 lists that match user data to db.
    # keys = kinase in DB, Phosphosite in DB, Subs_site in DB.
    # values = 3 lists of length of full phospho only data per key.
    # "kin_dict" = kinase entries that map to subs_sites in user data.
    # kinase = keys, subs_sites set per kinase = values.
    db_ud_dict, kin_dict = link_ud_to_db(filtered_df)
    
    # Pass "db_ud_dict" dictionary to dataframe.
    # 3 columns of length of full phospho only data returned.
    # Note: since "link_ud_to_db()" takes the full phospho data as input,
    # unpacking of the dictionary to dataframe returns columns, whose entries
    # match the order of the input. 
    db_ud_df = pd.DataFrame.from_dict(db_ud_dict, orient='index').transpose()
    
    # Concatenate full phospho table with DB user data matches.
    # Note: input dataframe "Filtered_df" index isn't ordered 1, 2, 3...,
    # due to previous operations. 
    # reset_index() extracts index to column, and uses default i.e. 1, 2, 3...,
    # as new index. Reseting the index is required, as dataframe
    # concatenation is by column indices!
    filtered_df = pd.concat([filtered_df.reset_index(drop=True),
                             db_ud_df.reset_index(drop=True)], 
                             axis=1)      
    
    # Sum control_cv & condition cv. 
    # User data that didn't contain cv columns upon original upload,
    # would return a sum of cv's equal to length of data frame.
    # This will distinguish it from user_data with CV columns present,
    # whose sum will always be unequal to length of data frame.
    sum_cont_cv = filtered_df.iloc[:, 10].sum()
    
    # Parse phospho-sites with corrected p-values <=0.05 & CV <=25% in both 
    # conditions or CV <=25% in either control or condition.
    # Parsed table passed to new data frame.
    # Note: if original user data upload didn't contain CV's then an alternate,
    # and simplified parsing rule used.
    if sum_cont_cv == len(filtered_df):
        filtered_signif_df = filtered_df.loc[filtered_df.iloc[:, 15]]
    else:
        filtered_signif_df = filtered_df.loc[filtered_df.iloc[:, 15] &
                                             filtered_df.iloc[:, 19] |
                                             filtered_df.iloc[:, 15] &
                                             filtered_df.iloc[:, 20] |
                                             filtered_df.iloc[:, 15] &
                                             filtered_df.iloc[:, 21]]
    
    # Replace "inf" & "-inf" values in log2 fold change column with nan.
    filtered_signif_df.loc[:, "Log2 fold change - condition over control"]\
                      .replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Replace nan with 0.
    filtered_signif_df.loc[:, "Log2 fold change - condition over control"] =\
    filtered_signif_df.iloc[:, 9].fillna(0)

    return(filtered_df, filtered_signif_df, kin_dict)

# --------------------------------------------------------------------------- #

### Function to extract and collate info from phospho data frame.
def data_extract(filtered_df, styno):
    """ Extract data groups as follows:
        1 - Proportion of phospho-sites in total data & % enrichment.
        2 - Frequency of phosphorylated residues.
        3 - Frequency of single & multiple phosphorylations.
        4 - Total number of proteins represented. """
    ### Data group - 1.
    # Compute length of phospho only dataframe.
    # Corresponds to number of phospho-sites.
    phos_site_num = len(filtered_df)

    # Compute length of full dataframe (including non-phosphos), 
    # minus number of phopho-peptides.
    # Corresponds to number of non-phosporylated peptides.
    non_phos_num = len(styno) - phos_site_num

    # Calculate % proportion of phospho-sites in total data-set.
    phos_perc_enrich = round((phos_site_num/(non_phos_num+phos_site_num)\
                              *100),1)

    # Create dictionary of variables.
    enrich_data_dict = {"phosphorylated": phos_site_num,
                        "Non-phosphorylated": non_phos_num,
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

### Function to analyse and visualise kinase data distributions. 
def kinase_analysis(db_kin_dict, parsed_sty_sort):
    """ Kinase centric analysis:
        1 - Global kinase and corresponding substrate_sites analysis:
        - Convert kinase dictionary from "ud_db_queries.py" to dataframe.
        - Extract groupings, totals and frequencies.
        2 - Significant phospho hits and corresponding kinase analysis:
        - Map signifcant phospho hits to matching kinases from db.
        - Calculate relative activity. """
    # ANALYSIS 1:
    # Call function to extract user/db data alignment as dictionaries.
    # Pass kinase dictionary to dataframe.
    # Df: index = kinases, columns = matching ("subs","site") string tuple(s).
    kin_subs_site_df = pd.DataFrame.from_dict(db_kin_dict, orient="index")
    
    # Pass kinase_dictionary keys to list variable and compute length.
    # This is the number of unique kinases whose substrates are detected
    # in the user data.
    unique_kin_lst_len = len(list(db_kin_dict.keys()))
    
    # Convert dataframe such that each row is now a 
    # unique substrate-site per kinase.
    # stack() - returns series of unique subs_sites per kinase. Index = kinases
    # to_frame() - converts series to dataframe.
    # reset_index() - extracts kinases from index to new column.
    # drop - removes "level_1" column (remnant of dictionary index structure).
    kin_subs_site_df = kin_subs_site_df.stack().\
                       to_frame().\
                       reset_index().\
                       drop("level_1", axis=1)
                       
    # Rename columns.
    kin_subs_site_df.columns = ["kinase", "subs_site"]
    
    # Concatenate "subs_site" tuple i.e. ('PRKDC', 'S2612') to "PRKDC_S2612".
    kin_subs_site_df["substrate_site"] =\
            ['_'.join(map(str, l)) for l in kin_subs_site_df["subs_site"]]  
                     
    # Drop string tuple.
    kin_subs_site_df = kin_subs_site_df.drop("subs_site", axis=1) 
    
    # Create dictionary from kin_subs_site_df:
    # Keys = Substrate_Site ID, Values = Series of kinases for each key.
    kin_subs_site_df_dict = kin_subs_site_df.groupby("substrate_site").\
                            kinase.agg(list).to_dict()
    
    # Pass substrates dictionary keys to list variable and compute length.
    # This is the number of unique subs_sites whose kinases are in the db.
    unique_subs_lst_len = len(list(kin_subs_site_df_dict.keys()))
    
    # Compute frequency of duplicate "Sub_site_ID" entries.
    # Series represents number of kinases that target a site in the user data.
    kinase_target_freq =\
             kin_subs_site_df.groupby([kin_subs_site_df.iloc[:, 1]]).size()
    
    # Compute sum of kinase frequencies.       
    kinase_target_entry_num = sum(kinase_target_freq)
    
    # Sort frequencies - highest to lowest.
    kinase_target_freq = kinase_target_freq.sort_values(ascending=False)
             
    # Take top 30 and pass to variable.
    kinase_target_freq = kinase_target_freq.head(n=30)
    
    # Compute frequency of duplicate kinases matched to user data.
    # Represents the total number of unique kinases, 
    # targeting a subs_site matched from db.
    kinase_freq =\
             kin_subs_site_df.groupby([kin_subs_site_df.iloc[:, 0]]).size()
    
    # Compute sum of subs_sites frequencies.
    Kinase_entry_num = sum(kinase_freq) 
    
    # Sort frequencies - highest to lowest.
    kinase_freq = kinase_freq.sort_values(ascending=False)
    
    # Take top 30 and pass to variable.
    kinase_freq = kinase_freq.head(n=30)
    
    # Parse subset of df corresponding to kinases & subs_sites.
    kin_word_list = kin_subs_site_df.iloc[:, 0]
    subs_sites_word_list = kin_subs_site_df.iloc[:, 1]
    
    # Convert subsets to string variables.
    # Format required to feed into wordcloud function.
    kin_word_str  = ' '.join(kin_word_list)               # Kinases.
    subs_sites_word_str  = ' '.join(subs_sites_word_list) # Substrate_sites.
    
    # ----------------------------------------------------------------------- #
    
    # ANALYSIS 2:
    # Parse significant hits table in the following order: gene, site_id,
    # log2 fold change & corrected p-value.
    signif_hits_subset = parsed_sty_sort[[parsed_sty_sort.columns[0],
                                          parsed_sty_sort.columns[1],
                                          parsed_sty_sort.columns[9],
                                          parsed_sty_sort.columns[13]]]
    
    # Parse hits with intensity in both conditions.
    signif_hits_subset =\
        signif_hits_subset[(signif_hits_subset.iloc[:, 2] > 0) |\
                           (signif_hits_subset.iloc[:, 2] < 0)]
        
    # Add column to signif phospho-sites table of 
    # concatenated substrate and site id.
    signif_hits_subset.loc[:,"substrate_site"] =\
        signif_hits_subset.iloc[:, 0].astype(str)+"_"+\
        signif_hits_subset.iloc[:, 1]
            
    # Drop 1st 2 columns.
    signif_hits_subset = signif_hits_subset.drop(["Substrate (gene name)", 
                                                  "Phospho site ID"], axis=1)
    
    # Merge significant hits dataframe subset and db query data
    # by "substrate_site" column.
    db_ud_merge_df =\
        pd.merge(kin_subs_site_df, signif_hits_subset, on="substrate_site")
    
    # Convert log2 fold changes to absolute values.
    db_ud_merge_df.loc[:, "Log2 fold change: absolute values"] =\
        db_ud_merge_df.iloc[:, 2].abs()     
    
    # Parse kinase and subs_sites to new column.
    kin_subs_only = db_ud_merge_df[[db_ud_merge_df.columns[0],
                                    db_ud_merge_df.columns[1]]]        
    
    # Calculate mean of absolute fold change per kinase
    kin_mean_abs_fold_change =\
        db_ud_merge_df.groupby("kinase")\
        ["Log2 fold change: absolute values"].mean()
         
    # Calculate sum of log2 fold changes per kinase
    kin_sum_fold_change =\
        db_ud_merge_df.groupby("kinase")\
        ["Log2 fold change - condition over control"].sum()
    
    # Concatenate kinase activity estimates.
    kin_activity_merge = pd.concat([kin_mean_abs_fold_change,
                                    kin_sum_fold_change], axis=1)
    
    # Change column names.
    kin_activity_merge.columns = ["Kinase activity: mean of absolute fold changes",
                                  "Kinase activity: sum of fold changes"]
    
    # Change sign of mean absolute fold changes by the sign in the
    # sum of fold changes and parse to new variable.
    kin_activity_merge.iloc[:, 0][kin_activity_merge.iloc[:, 1]<0] *= -1
    
    # Parse mean of absolute fold changes with sign change to new column.
    kin_activities = kin_activity_merge[[kin_activity_merge.columns[0]]]
    
    # Set kinase names to column instead of index.
    kin_activities.reset_index(level=0, inplace=True)
    
    # Group kinases in db & user data merged df as dictionary:
    # Keys = Kinases
    # values = subs_sites
    kin_subs_dict = kin_subs_only.groupby("kinase").\
                                substrate_site.agg(list).to_dict()
    
    # Map Kinase activities to the subs_sites from which they are calculated.
    # Kinase column in df mapped to keys (kinases) in dictionary.
    kin_activities.loc[:, "Substrate_site"] =\
        kin_activities["kinase"].map(kin_subs_dict)
    
    # Reorder columns.
    kin_activities =\
        kin_activities[["kinase", 
                        "Substrate_site", 
                        "Kinase activity: mean of absolute fold changes"]]
    
    # Sort values - log2 fold change lowest to highest.
    kin_activities =\
        kin_activities.\
        sort_values(by=["Kinase activity: mean of absolute fold changes"], 
                    ascending=False)
    
    # Convert "Substrate_site" list entries to string and split by ",".
    # Removes [] & '' characters from column entries.
    kin_activities["Substrate_site"] =\
        kin_activities["Substrate_site"].apply(", ".join)
        
    return(kinase_target_freq,  # Substrate_sites frequencies.
           kinase_freq,         # Kinase frequencies.
           kin_word_str,        # Kinase word string for wordcloud.
           subs_sites_word_str, # Substrate_sites word string for wordcloud.
           kin_activities)      # Kinase activities for styler.
        
# --------------------------------------------------------------------------- #

# set up run if running this script only
if __name__ == "__main__":

    #set up runs for testing functions
    file = os.path.join('user_data', 'az20.tsv')

    data_or_error = user_data_check(file)
    
    styno, sty = create_filtered_dfs(data_or_error)

    corrected_p = correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort, db_kin_dict = table_sort_parse(corrected_p)

    phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq =\
    data_extract(full_sty_sort, styno)
    
    kinase_target_freq, kinase_freq, kin_word_str, subs_sites_word_str,\
    kinase_activities = kinase_analysis(db_kin_dict, parsed_sty_sort)
    
# --------------------------------------------------------------------------- #