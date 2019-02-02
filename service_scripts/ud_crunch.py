"""Carmen's version of Alex's data crunch script to put into functions
 ready to receive uploaded data-TEST VERSION"""

# Import packages into environment.
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib as mpl
from statsmodels.stats.multitest import fdrcorrection


def create_filtered_dfs(datafile):
    """ Create data frame subsets of user data and expand
    with further analysis"""
    # Read user_data and assign to dataframe variable.
    ud_df_orig = pd.read_table(datafile)
    # Parse data that contains at least 1 quant value in either condition and
    # pass to variable.Note: "df.iloc" function used to specify column indices
    # instead of column names. Allows for  different field names.
    ud_df1_quant = ud_df_orig[(ud_df_orig.iloc[:, 1] > 0) | \
                            (ud_df_orig.iloc[:, 2] > 0)]

    # Copy phospho-site id from "Substrate" field and append to new column.
    ud_df1_quant["Phospho_site_ID"] = ud_df1_quant.iloc[:, 0].\
                            str.extract(r"\((.*?)\)", expand=False)

    # Remove Phospho-site ID including () from "Substrate" column
    ud_df1_quant.iloc[:, 0] = ud_df1_quant.iloc[:, 0].\
                            str.replace(r"\(.*\)", "")

    # Parse data that contains only Ser, Thr, Tyr & non phospho-sites (STYN).
    ud_df2_styn = ud_df1_quant[ud_df1_quant.iloc[:, 7].
                            str.contains("S|T|Y|None", case=False)]
    # Search not case sensitive.
    # Parse data that contains Ser, Thr & Tyr phospho-sites only (STT)
    ud_df3_sty = ud_df2_styn[ud_df2_styn.iloc[:, 7].
                            str.contains("S|T|Y", case=False)]

    # Parse data for phospo-sites with valid p-values.
    ud_df4_sty_valid = ud_df3_sty[(ud_df3_sty.iloc[:, 4] > 0)]

    # Find max values of control vs input protein means, column header names
    cond_1_name = ud_df4_sty_valid.columns[1]
    cond_2_name = ud_df4_sty_valid.columns[2]
    condition_max = ud_df4_sty_valid[[cond_1_name, cond_2_name]].max(
        axis=1)  # Find max of row for the 2 conditions.

    # Calculate "fold conditions over max" values and append to new columns.
    # "df.divide" used to divide individual elements in a column by a variable.
    ud_df4_sty_valid["Fold_control_over_max"] =\
                    ud_df4_sty_valid.iloc[:, 1].divide(condition_max, axis=0)
    ud_df4_sty_valid["Fold_condition_over_max"] =\
                    ud_df4_sty_valid.iloc[:, 2].divide(condition_max, axis=0)

    # Calc log2 fold change - condition/control append as new column to df.
    ud_df4_sty_valid["Log2 fold change - condition over control"] =\
                                    np.log2(ud_df4_sty_valid.iloc[:, 3])

    # List of ordered column indices - not dependent on column names!
    new_col_order = [0, 7, 1, 2, 8, 9, 3, 10, 4, 5, 6]

    # List comprehension to re-order df columns by new index list.
    ud_df5_final = ud_df4_sty_valid[[ud_df4_sty_valid.columns[i]
                                     for i in new_col_order]]

    return(ud_df2_styn, ud_df4_sty_valid, ud_df5_final)


# function to take final filtered Df from create_filtered_dfs function
def correct_pvalue(filtered_df):
    """Correct p-value for multiple testing errors
    Pass p-value series to "fdrcorrection" function.
    Benjamini/Hochberg: independent or positively correlated  tests.
    Benjamini/Yekutieli: general or negatively correlated tests.
    "rej_hyp" = rejected null hypotheses as array list of boolean values.
    "corr_p_value" = array  of corrected p-values in original series order."""

    rej_hyp, corr_p_val = fdrcorrection(filtered_df.iloc[:, 8],
                              alpha=0.05)  # alpha = permissable error rate.

    # Convert "rej_hyp" & "corr_p_value" to data-frames.
    rej_hyp_df = pd.DataFrame(rej_hyp)
    corr_p_val_df = pd.DataFrame(corr_p_val)

    # Take -log10 of the corrected p-value.
    neg_log10_corr_p_val = (np.log10(corr_p_val_df)) * -1

    # Append "rej_hyp", "corr_p_val" & "neg_log10_corr_p_val" values to new column.
    filtered_df["corrected_p_value"] = corr_p_val_df.values
    filtered_df["rejected_hypotheses"] = rej_hyp_df.values

    # Sort data frame by ascending p-values i.e. smallest to largest.
    filtered_df = filtered_df.sort_values(filtered_df.columns[11])

    # Sort -log10(p-values) in descending order i.e. smallest p-values will have largest log10 values.
    neg_log10_corr_p_val = neg_log10_corr_p_val.sort_values(0, ascending=False)

    # Append -log10(p-values) to new column in data frame.
    # Note: "df.assign" function used for appending new column!
    # Standard column append method re-orders values and leads to mis-match of p-values.
    filtered_df = filtered_df.assign(neg_log10_corr_p_values=
                                     neg_log10_corr_p_val.values)

    return(filtered_df)

#TODO work on "functionifying" the rest of te data crunch script
##-------------------------------------------------------------------------------------------------------------------------##

######################################################################
### Data frame expansion & sorting of filtered phospho-sites table ###
######################################################################

##-------------------------------------------------------------------------------------------------------------------------##

# set up run if running this script only
if __name__ == "__main__":

    #set up runs for testing functions
    file = 'user_data.txt'

    styn, sty, filtered = create_filtered_dfs(file)

    corrected_p = correct_pvalue(filtered)

    print(corrected_p)
