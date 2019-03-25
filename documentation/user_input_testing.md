## User Input Testing 

This document displays a number of example searches that constitute user input data in different formats. 

i) [User input AZ20.tsv](user_input_testing.md#test-case-scenario-1)

ii) [User input AZ20.tsv, however missing the CV column](user_input_testing.md#test-case-scenario-2)

iii) [User input AZ20.tsv, however CV column is in a random location](user_input_testing.md#test-case-scenario-3)

iv) [User input AZ20.tsv, however the residue type and number does not contain any 'nones'](user_input_testing.md#test-case-scenario-4)

v) [User input AZ20.tsv, however the substrate name column has been placed as the final column](user_input_testing.md#test-case-scenario-5)

vi) [User input AZ20.tsv, however the substrate name column has been placed in a random position](user_input_testing.md#test-case-scenario-6)

vii) [User input AZ20.tsv, however the p values column is missing](user_input_testing.md#test-case-scenario-7)

viii) [User input AZ20.tsv, however the p values column is in a random column](user_input_testing.md#test-case-scenario-8)

ix) [User input AZ20.tsv, however the fold values column is missing](user_input_testing.md#test-case-scenario-9)

x) [User input AZ20.tsv, however the fold values column has been moved to a different column](user_input_testing.md#test-case-scenario-10)


#### Test case scenario 1 = User input AZ20.tsv 

![Search for AZ20.tsv](images/user_data_testing/User1a.png)

Results for AZ20.tsv are as follows with no error messages displayed.  

![Results for AZ20.tsv](images/user_data_testing/User1b.png)
 

#### Test case scenario 2 = User input AZ20.tsv, however missing the CV column 

![Search for AZ20.tsv_noCSVcolumn](images/user_data_testing/User2a.png)  
 
Results for AZ20.tsv without the CV column. Here, the data analysis is still performed, however if the original file does not include a CV column, then only the p-value threshold is applied towards the calculation.   

![Results for AZ20.tsv_noCSVcolumn](images/user_data_testing/User2b.png)


#### Test case scenario 3 = User input AZ20.tsv, however the CV column is in a random location 

![Search for AZ20.tsv_cvs_moved](images/user_data_testing/User3a.png)  
  
Results for AZ20.tsv with the CV columns in a different location. Here, the data analysis does not perform, as it expects the CV columns to be at the end fo the user data file. 

![Results for AZ20.tsv_cvs_moved](images/user_data_testing/User3b.png)
 
 
#### Test case scenario 4 = User input AZ20.tsv, however the residue type and number does not contain any 'nones'

![Search for AZ20.tsv_noNones](images/user_data_testing/User4a.png) 
  
Results for AZ20.tsv_noNones show that the analysis functions as normal and the lack of 'nones' within the substrate column does not affect the analysis.
 
![Results for AZ20.tsv_noNones](images/user_data_testing/User4b.png)


#### Test case scenario 5 = User input AZ20.tsv, however the substrate name column has been placed as the final column

![Search for AZ20.tsv_substrateColumn_asFinalColumn](images/user_data_testing/User5a.png) 

Results for AZ20.tsv_substrateColumn_asFinalColumn show that the current analysis requires the substrate name information to be as the first column of the user input file. 

![Results for AZ20.tsv_substrateColumn_asFinalColumn](images/user_data_testing/User5b.png)

#### Test case scenario 6 = User input AZ20.tsv, however the substrate name column has been placed in a random position

![Search for AZ20.tsv_substrateColumn_asRandomColumn](images/user_data_testing/User6a.png) 

Results for AZ20.tsv_substrateColumn_asRandomColumn show that the current analysis requires the substrate name information to be as the first column of the user input file. 

![Results for AZ20.tsv_substrateColumn_asRandomColumn](images/user_data_testing/User6b.png)

#### Test case scenario 7 = User input AZ20.tsv, however the p values column is missing

![Search for AZ20.tsv_missingPvalues](images/user_data_testing/User7a.png) 

Results for AZ20.tsv_missingP values show that the current analysis requires a P value column to be present for the analysis to be completed.  

![Results for AZ20.tsv_missingPvalues](images/user_data_testing/User7b.png)

#### Test case scenario 8 = User input AZ20.tsv, however the p values column is in a random column

![Search for AZ20.tsv_Pvalues_asRandomColumn](images/user_data_testing/User8a.png) 

Results for AZ20.tsv_missingPvalues show that the current analysis requires a P value column to be present for the analysis to be completed.  

![Results for AZ20.tsv_Pvalues_asRandomColumn](images/user_data_testing/User8b.png)


#### Test case scenario 9 = User input AZ20.tsv, however the fold values column is missing

![Search for AZ20.tsv_missingFoldvalues](images/user_data_testing/User9a.png) 

Results for AZ20.tsv_missingFoldvalues show that the current analysis requires a Fold value column to be present for the analysis to be completed.  

![Results for AZ20.tsv_missingFoldvalues](images/user_data_testing/User9b.png)

 #### Test case scenario 10 = User input AZ20.tsv, however the fold values column has been moved to a different column

![Search for AZ20.tsv_FoldValues_asRandomColumn](images/user_data_testing/User10a.png) 

Results for AZ20.tsv_FoldValues_asRandomColumn show that the current analysis requires a Fold value column to be present in the expected column.  

![Results for AZ20.tsv_FoldValues_asRandomColumn](images/user_data_testing/User10b.png)











