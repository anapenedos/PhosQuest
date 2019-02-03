"""scripts to format subsets of crunched data for display"""
from service_scripts import ud_crunch
import pandas as pd

def display_basic(filename):
   """Run first two functions in ud_crunch and output
                  final corrected dataframe"""
   # run initial filtering script
   dataframes = ud_crunch.create_filtered_dfs(filename)

    #run P-value correction on filtered df
   p_correct = ud_crunch.correct_pvalue(dataframes[2])

   #create subset of some columns for display
   basic_display_only = p_correct.copy()
   # delete un-needed columns for display
   basic_display_only = basic_display_only.drop(basic_display_only.columns[[3,
                                        4, 12]], axis=1)

   # remove underscores for display
   #
   basic_display_only.iloc[0, :] = \
      basic_display_only.iloc[0,:].str.replace("_", " ")

   basic_display_only = basic_display_only.to_html()
   #return formatted display data and original dataframes
   return [basic_display_only, dataframes, p_correct]


