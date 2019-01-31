#################################
## User data processing script ##
#################################

##-------------------------------------------------------------------------------------------------------------------------##

# Import packages into environment.
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib as mpl
from statsmodels.stats.multitest import fdrcorrection

##-------------------------------------------------------------------------------------------------------------------------##

###############################################################################
### Create data frame subsets of user data and expand with further analysis ###
###############################################################################

##-------------------------------------------------------------------------------------------------------------------------##

# Read user_data into enviornment and assign to dataframe variable.
ud_df_a = pd.read_table("../service_scripts/user_data.txt")

# Parse data that contains at least 1 quantitation value in either condition and pass to variable.
# Note: "df.iloc" function used to specify column indices instead of column names.
# This method is more robust as user data will certainly have different names for fields.
ud_df_b = ud_df_a[(ud_df_a.iloc[:, 1]>0) | (ud_df_a.iloc[:, 2]>0)]

# Copy phospho-site id from "Substrate" field and append to new column.
ud_df_b["Phospho_site_ID"] = ud_df_b.iloc[:, 0].str.extract(r"\((.*?)\)", expand=False)

# Remove Phospho-site ID including () from "Substrate" column and replace with empty string.
ud_df_b.iloc[:, 0] = ud_df_b.iloc[:, 0].str.replace(r"\(.*\)","")

# Parse data that contains Serine, Threonine, Tyrosine & non phospho-sites only.
ud_df_c = ud_df_b[ud_df_b.iloc[:, 7].str.contains("S|T|Y|None", case=False)]  # Search for these string elements.
                                                                              # Search not case sensitive.
                                                                                   
# Parse data that contains Serine, Threonine & Tyrosine phospho-sites only.
ud_df_d = ud_df_c[ud_df_c.iloc[:, 7].str.contains("S|T|Y", case=False)]

# Parse data for phospo-sites with valid p-values.
ud_df_e = ud_df_d[(ud_df_d.iloc[:, 4]>0)]

# Find max values of control vs AZ20 means.
cond_1_name = ud_df_e.columns[1]                                 # Pass column header at column index 1 to new variable.
cond_2_name = ud_df_e.columns[2]                                 # Pass column header at column index 2 to new variable.
condition_max = ud_df_e[[cond_1_name, cond_2_name]].max(axis=1)  # Find max of row for the 2 conditions.

# Calculate "fold conditions over max" values and append them to new columns.
# Note: "df.divide" function used to divide individual elements in a column by a variable.
ud_df_e["Fold_control_over_max"] = ud_df_e.iloc[:, 1].divide(condition_max, axis=0)  
ud_df_e["Fold_condition_over_max"] = ud_df_e.iloc[:, 2].divide(condition_max, axis=0)

# Calculate log2 fold change - AZ20 over control and append as new column to data frame.
ud_df_e["Log2 fold change - AZ20 over control"] = np.log2(ud_df_e.iloc[:, 3])

# Specify a new list of ordered column indices - not dependent on column names!
new_col_order = [0, 7, 1, 2, 8, 9, 3, 10, 4, 5, 6]    

# List comprehension to re-order df columns by new index list.          
ud_df_f = ud_df_e[[ud_df_e.columns[i] for i in new_col_order]]  
                                                                                                                                
##-------------------------------------------------------------------------------------------------------------------------##

###################################################
### Correct p-value for multiple testing errors ###
###################################################

##-------------------------------------------------------------------------------------------------------------------------##

# Pass p-value series to "fdrcorrection" function. 
# Benjamini/Hochberg: independent or positively correlated  tests.
# Benjamini/Yekutieli: general or negatively correlated tests.
# "rej_hyp" = rejected null hypotheses as array list of boolean values.
# "corr_p_value" = array list of corrected p-values in original series order.
rej_hyp, corr_p_val = fdrcorrection(ud_df_f.iloc[:, 8], 
                                    alpha=0.05)  # alpha = permissable error rate.

# Convert "rej_hyp" & "corr_p_value" to data-frames.
rej_hyp_df = pd.DataFrame(rej_hyp)
corr_p_val_df = pd.DataFrame(corr_p_val)

# Take -log10 of the corrected p-value.
neg_log10_corr_p_val = (np.log10(corr_p_val_df))*-1
 
# Append "rej_hyp", "corr_p_val" & "neg_log10_corr_p_val" values to new column.
ud_df_f["corrected_p_value"] = corr_p_val_df.values
ud_df_f["rejected_hypotheses"] = rej_hyp_df.values 

# Sort data frame by ascending p-values i.e. smallest to largest.
ud_df_f = ud_df_f.sort_values(ud_df_f.columns[11])

# Sort -log10(p-values) in descending order i.e. smallest p-values will have largest log10 values.                          
neg_log10_corr_p_val = neg_log10_corr_p_val.sort_values(0, ascending=False)

# Append -log10(p-values) to new column in data frame.
# Note: "df.assign" function used for appending new column!  
# Standard column append method re-orders values and leads to mis-match of p-values.  
ud_df_f = ud_df_f.assign(neg_log10_corr_p_values=neg_log10_corr_p_val.values)  

##-------------------------------------------------------------------------------------------------------------------------##

######################################################################
### Data frame expansion & sorting of filtered phospho-sites table ###
######################################################################

##-------------------------------------------------------------------------------------------------------------------------##

# Phospho-sites detected in single conditions and append to new columns.
ud_df_f["control"] = ((ud_df_f.iloc[:, 2]>0) & (ud_df_f.iloc[:, 3]==0))    # control only.
ud_df_f["condition"] = ((ud_df_f.iloc[:, 2]==0) & (ud_df_f.iloc[:, 3]>0))  # AZ20 only.

# Phospho-sites detected in both conditions and append to new column.
ud_df_f["both"] = ((ud_df_f.iloc[:, 2]>0) & (ud_df_f.iloc[:, 3]>0))

# Sort data frame
sort_level_1 = ud_df_f.columns[12]                 # Rejected hypotheses.
sort_level_2 = ud_df_f.columns[14]                 # Sites in only control.
sort_level_3 = ud_df_f.columns[15]                 # Sites in only AZ20.
sort_level_4 = ud_df_f.columns[16]                 # Sites in both conditions.
sort_level_5 = ud_df_f.columns[7]                  # Log2 fold change.
ud_df_f = ud_df_f.sort_values(by=[sort_level_1, 
                               sort_level_2, 
                               sort_level_3, 
                               sort_level_4, 
                               sort_level_5], 
                           ascending=False)        # Boolean sorting - true hits at top.

# Parse phospho-sites with corrected p-values <=0.05 and pass to new variable.
ud_df_g = ud_df_f[(ud_df_f.iloc[:, 11]<=0.05)]
ud_df_g.to_csv("../user_data/significant_hits.csv")

##-------------------------------------------------------------------------------------------------------------------------##

##############################################
### Data extraction for feeding into plots ###
##############################################

##-------------------------------------------------------------------------------------------------------------------------##

# Calculate proportion of phospho-sites in total data-set. 
# Note: this serves as a good proxy for a %enrichment estimation. 

# Number of phospho-sites. 
phos_site_num = len(ud_df_d)            

# Number of non-phosporylated peptides.
non_phos_num = len(ud_df_c) - phos_site_num  

# Calculate % proportion of phospho-sites in total data-set.
phos_perc_enrich = round((phos_site_num/(non_phos_num+phos_site_num)*100),1)

##-------------------------------------------------------------------------------------------------------------------------##

# Calculate frequency of each phospho AA residue - case insensitive.
phos_ser = sum(ud_df_f.iloc[:, 1].str.contains("S", case=False))  # Serine.
phos_thr = sum(ud_df_f.iloc[:, 1].str.contains("T", case=False))  # Threonine.
phos_tyr = sum(ud_df_f.iloc[:, 1].str.contains("Y", case=False))  # Tyrosine.

##-------------------------------------------------------------------------------------------------------------------------##

# Count frequency of multiply phosphorylated residues in either condition.
# Note: duplicate intensities for the same substrate denotes that the same peptide has multiple phospho-residues.
# Counting frequency of duplicates therefore represents the distribution of multiply-phosphorylated residues.
# Create data frame with 3 fields from main data frame.
phos_df_subset = ud_df_f[[ud_df_f.columns[0],   # Substrate.
                          ud_df_f.columns[2],   # control_mean.
                          ud_df_f.columns[3]]]  # AZ20_mean.

# Parse hits unique to each condition.
phos_df1_subset_unique = phos_df_subset.loc[(phos_df_subset.iloc[:, 1]>0) & 
                                            (phos_df_subset.iloc[:, 2]==0)]  # control mean.
phos_df2_subset_unique = phos_df_subset.loc[(phos_df_subset.iloc[:, 2]>0) & 
                                            (phos_df_subset.iloc[:, 1]==0)]  # AZ20_mean.

# Parse hits with all intensities reported in both conditions.
# Note: multiply phosphorylated residues will have duplicate intensities in both conditions,
# though not necessarily the same intensities. 
phos_df_subset_complete = phos_df_subset.loc[(phos_df_subset.iloc[:, 1]>0) & (phos_df_subset.iloc[:, 2]>0)]


# "df.groupby" function used to return groups of a series (default = by rows).
# In this case the series is a list of intensities, which is grouped by duplicates.
# "groupby.size" function computes group sizes i.e. frequency of each duplicate group.
phos_df1_unique_groups = phos_df1_subset_unique.groupby([phos_df1_subset_unique.iloc[:, 0], 
                                                         phos_df1_subset_unique.iloc[:, 1]]).size()     # control_mean.

phos_df2_unique_groups = phos_df2_subset_unique.groupby([phos_df2_subset_unique.iloc[:, 0], 
                                                         phos_df2_subset_unique.iloc[:, 2]]).size()     # AZ20_mean.

phos_df_complete_groups = phos_df_subset_complete.groupby([phos_df_subset_complete.iloc[:, 0], 
                                                           phos_df_subset_complete.iloc[:, 1],
                                                           phos_df_subset_complete.iloc[:, 2]]).size()  # complete.
                                                                                              
# Compute summary of AA phos residue frequencies for unique and complete hits.
phos_df1_unique_res_freq = phos_df1_unique_groups.value_counts()    # control_mean unique hits frequencies
phos_df2_unique_res_freq = phos_df2_unique_groups.value_counts()    # AZ20_mean unique hits frequencies
phos_df_complete_res_freq = phos_df_complete_groups.value_counts()  # complete hits frequencies

# Concatenate frequency series for each category. 
total_res_freq_df = pd.concat([phos_df1_unique_res_freq, 
                               phos_df2_unique_res_freq, 
                               phos_df_complete_res_freq], axis=1)  # "axis" sets joing along columns - default = rows.

# Sum all frequency series to compute total multiply phosphorylated residues.
total_res_freq_summary = total_res_freq_df.sum(axis=1)

##-------------------------------------------------------------------------------------------------------------------------##

####################################################################################
### Plot heatmap of most significant, differentially expressed phospho site hits ###
####################################################################################

##-------------------------------------------------------------------------------------------------------------------------##

# Combine concatenated column with conditionfold over max columns.
signif_hits_subset = ud_df_g[[ud_df_g.columns[0],   # Substrate.
                              ud_df_g.columns[1],   # Phospho_site_ID.
                              ud_df_g.columns[4],   # Fold_control_over_max.
                              ud_df_g.columns[5]]]  # Fold_condition_over_max.    

# Concatenate "Substrate" & "Phospho_site_ID" into one column and append to new column.
signif_hits_subset["Phospho_site_ID"] = signif_hits_subset.iloc[:, 0].astype(str)+"_"+signif_hits_subset.iloc[:, 1]

# Pass subset to new variable.
signif_hits_subset = signif_hits_subset[[signif_hits_subset.columns[1],
                                         signif_hits_subset.columns[2],   
                                         signif_hits_subset.columns[3]]]

# Set "Phospho_site_ID" as index and parse the fold over max values
signif_hits_subset = signif_hits_subset.set_index(signif_hits_subset.iloc[:, 0].values)
signif_hits_subset = signif_hits_subset[[signif_hits_subset.columns[1],
                                         signif_hits_subset.columns[2]]]

# Plot heatmap of most significant hits - "Substrate", "Fold_control_over_max" & "Fold_condition_over_max"
# TESTINT, TESTING - could do with some work.
fig = mpl.pyplot.figure(figsize=(16,48))
fig.subplots_adjust(right=0.4)
test = sb.heatmap(signif_hits_subset, cmap="YlGnBu", cbar_kws={"shrink":0.25})
fig.savefig("test.png")

##-------------------------------------------------------------------------------------------------------------------------##                                                                  