# Web App Testing 

Disclaimer - Please note all User Input testing was performed under an initial name, which has since been modified to PhosQuest.

This document displays a number of example searches that constitute our web app testing. Web app testing was performed using a number of test inputs under the 'similar matches' and 'exact matches' options. The results of both are listed for each search. As a rule of thumb, if any search is performed under the wrong selection options, or with an input that was not present in the database, the following message would be displayed e.g. searching for a something as an inhibitor when it is not:-

![NoresultsFound](images/web_app_testing/notfound.png)

  **Searching via 'similar matches' and 'exact matches' options**

i) [Searching for kinase accession number e.g. Q9BQI3](web_app_testing.md#test-case-scenario-1--searching-for-kinase-accession-number-eg-q9bqi3)
 
ii) [est case scenario 2 = Searching for kinase accession name - HRI](web_app_testing.md#test-case-scenario-2--searching-for-kinase-accession-name---hri)

iii) [Test case scenario 3 = Searching for substrate via accession name e.g. P01236](web_app_testing.md#test-case-scenario-3--searching-for-substrate-via-accession-name-eg-p01236)

iv) [Test case scenario 4 = Searching for kinase accession name - e.g. PRL](web_app_testing.md#test-case-scenario-4--searching-for-kinase-accession-name---eg-prl)

v) [Test case scenario 5 = Searching for Inhibitors via accession number e.g. 4877](web_app_testing.md#test-case-scenario-5--searching-for-inhibitors-via-accession-number-eg-4877)
 
 vi) [Test case scenario 6 = Searching for Inhibitors via name e.g. (5Z)-7-Oxozeaenol](web_app_testing.md#test-case-scenario-6--searching-for-inhibitors-via-name-eg-5z-7-oxozeaenol)
 
 
<br></br>
### Test case scenario 1 = Searching for kinase accession number e.g. Q9BQI3

**'Similar Matches' option**

![Search for Q9BQI3](images/web_app_testing/Case1a.png)

Results for Q9BQI3 and related Phosphosites 

![Results for Q9BQI3](images/web_app_testing/Case1b.png)

Selecting one of the Group IDs (e.g. 447635) leads to a detailed display of this particular group of phosphosites. 

![Results for Q9BQI3](images/web_app_testing/Case1c.png)

Here we also see a list of kinases which are related to this specific phosphosite (447635). In this list we can observe the original kinase (Q9BQI3) which we had searched for, allowing us to link back to the original search. 

**'Exact Matches' option**
<br> For the exact matches option, the identical results were observed. 

<br></br>
### Test case scenario 2 = Searching for kinase accession name - HRI

**'Similar Matches' option**

![Search for HRI](images/web_app_testing/Case2a.png) 

Results for HRI and kinase records. 

![Results for HRI](images/web_app_testing/Case2b.png)

Selecting one of the specific kinase accession numbers e.g. P29323 gives further detailed information regarding that particular kinase. 

![Results for HRI](images/web_app_testing/Case2c.png)

From here, one can link to the specific phosphosites related to this particular kinsase. Selecting the detail tab, it is possible to go into the full details of this particular phosphosite:-
 
![Results for HRI](images/web_app_testing/Case2d.png)

And from here, one can observe the kinases associated with this phosphosite, and link back to the original EPHB2 search result (Accession number P29323)

**'Exact Matches' option**
<br> For the exact matches option, HRI was not detected because the "name searches" utilises kinases = `kin_full_name`, which translates to full name. Thus, searching for HRI will not work in an exact match as this corresponds to gene name. Currently we could only search for one specific field. In the future, we will look to implement multi-field searches to capture different information. 

<br></br>
### Test case scenario 3 = Searching for substrate via accession name e.g. P01236

**'Similar Matches' option**

![Search for P01236](images/web_app_testing/Case3a.png)
 
Results for P01236 and phosphosites related to this particular substrate.

![Results for P01236](images/web_app_testing/Case3b.png)

Selecting one of the Group IDs (e.g. 451732) leads to a detailed display of characterisitcs relating to this particular group of phosphosites. 

![Results for P01236](images/web_app_testing/Case3c.png)

Here, we can view detailed information regarding the selected phosphosite group. We also have the "related substrate" qualifer, and this takes us back to the previous page.  

**'Exact Matches' option**
<br> For the exact matches option, the identical results were observed. 

<br></br>
### Test case scenario 4 = Searching for kinase accession name - e.g. PRL

**'Similar Matches' option**

![Search for PRL](images/web_app_testing/Case4a.png) 

Results for PRL substrate records. 

![Results for PRL](images/web_app_testing/Case4b.png)

Selecting one of the specific substrate accession numbers e.g. Q8WTW4 gives further detailed information regarding that particular substrate. 

![Results for PRL](images/web_app_testing/Case4c.png)

From here, one can link to phosphosites related to this particular substrate. Selecting the detail tab, it is possible to view the full details of this particular phosphosite:-
 
![Results for PRL](images/web_app_testing/Case4d.png)

From here, one can select the related substrates and go back to the substrates table.

![Results for PRL](images/web_app_testing/Case4e.png)

**'Exact Matches' option**
<br> For the exact matches option, PRL was not detected. The "name searches" utilises substrates = `subs_full_name`, which translates to full name. Thus, searching for PRL will not work in an exact match as this corresponds to gene name. Currently we could only search for one specific field. In the future, we will look to implement multi-field searches to capture different information. 

<br></br>
### Test case scenario 5 = Searching for Inhibitors via accession number e.g. 4877

**'Similar Matches' option**

![Search for 4877](images/web_app_testing/Case5a.png)

Results for 4877 and a list of potential PubChem numbers. 

![Results for 4877](images/web_app_testing/Case5b.png)

Selecting one of the Group IDs (e.g. 4877) leads to a detailed display of characterisitcs relating to this particular inhibitor. 

![Results for 4877](images/web_app_testing/Case5c.png)

**'Exact Matches' option**
<br> For the exact matches option, the search result did not produce the table of the three options but actually directly displayed the resutls for 4877. 

<br></br>
 ### Test case scenario 6 = Searching for Inhibitors via name e.g. (5Z)-7-Oxozeaenol

**'Similar Matches' option**

![Search for (5Z)-7-Oxozeaenol](images/web_app_testing/Case6a.png)

Results for (5Z)-7-Oxozeaenol. 

![Results for (5Z)-7-Oxozeaenol](images/web_app_testing/Case6b.png)

<br></br>
**'Exact Matches' option**
<br> For the exact matches option, the identical results were observed. The exact match functioned as expected here since "name searches" utilizes inhibitor - `inhib_name` which translates to 'other name' for inhibitors and this worked successfully for the input used here. 

**Summary** 

In this short web app testing, we have tested the pipeline of searches for the six main methods of searches using similar and exact search options:-
- Kinase with accession or ID
- Kinase with name
- Substrate with accession or ID
- Substrate with name
- Inhibitor with accession of ID
- Inhibitor with name

Currently we there are slight issues for the Kinase and Substrate searches, when names are used, with the 'exact matches' option based upon the field used to search for. In the future, we will look to implement multi-field searches to capture different information. We also tried a number of random character inputs and for all occasions, and this was captured with the default display "sorry no results found".

We have tried to graphically illustrate the results of such searches and demonstrate that all links and searches work as expected. In the future we hope to implement an even more comprehensive web app testing document. 


