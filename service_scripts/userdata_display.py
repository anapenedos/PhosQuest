"""scripts to display subsets of crunched data"""
from service_scripts import ud_crunch
import pandas as pd

def display_basic(filename):
   """Run first two functions in ud_crunch and output
                  final corrected dataframe"""
   dataframes = ud_crunch.create_filtered_dfs(filename)
   filtered_df = dataframes[2]# just filtered_df needed now
   p_correct = ud_crunch.correct_pvalue(filtered_df)
   #create subset of some columns for display
   basic_display_only = p_correct.copy()
   basic_display_only = basic_display_only.rename(columns=
            {'corrected_p_value': 'Corrected P-value',
                   'neg_log10_corr_p_values': '-Log10 corrected P-value'})

   basic_display_only = basic_display_only.to_html()
   return [basic_display_only, p_correct]