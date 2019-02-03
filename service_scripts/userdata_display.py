"""scripts to format subsets of crunched data for display"""
from service_scripts import ud_crunch
import pandas as pd

def display_basic(filename):
   """Run first two functions in ud_crunch and output
                  final corrected dataframe"""
   # run initial filtering script
   dataframes = ud_crunch.create_filtered_dfs(filename)

   filtered_df = dataframes[2]# just filtered_df needed now

   #run P-value correction
   p_correct = ud_crunch.correct_pvalue(filtered_df)

   #create subset of some columns for display
   basic_display_only = p_correct.copy()
   # delete un-needed columns for display
   basic_display_only = basic_display_only.drop(basic_display_only.columns[[3,
                                        4, 12]], axis=1)

   # remove underscores for display *****TEST ONLY WONT WORK FOR ALL???*****
   change_columns = {'Fold_condition_over_max':'Fold condition over max',
              'AZ20_fold_change':'Fold change',
              'AZ20_p-value':'p-value',
              'AZ20_ctrlCV':'control CV',
              'AZ20_treatCV':'AZ20_treatCV',
              'corrected_p_value': 'Corrected P-value',
              'neg_log10_corr_p_values': '-Log10 corrected P-value'}

   basic_display_only = basic_display_only.rename(columns = change_columns)

   basic_display_only = basic_display_only.to_html()
   #return formatted display data and original dataframes
   return [basic_display_only, dataframes, p_correct,]