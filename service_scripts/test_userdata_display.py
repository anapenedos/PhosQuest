"""Test script to import Alex's processed data excel file into pd
dataframe and display display columns in some form on website."""

import pandas as pd

#TODO update to pull partial data into separate tables and display

def xl_to_html(excel_file):
   """function to convert pandas dataframe to html"""
   df = pd.read_excel(excel_file)

   return  df.to_html()




