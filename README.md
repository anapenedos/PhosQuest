# PhosphoQuest Application Readme

## Website functionality - Basic overview
PhosphoQuest is a web application designed to enable users to search and browse a compiled database containing information about Human protein kinases, their substrates and inhibitors with related phosphosite and disease information. 

The application also provides an area for users to upload a tsv or csv file of experimental phosphorylation data and receive the significantly up or down phosphorylated sites, and other useful analysis. The analysed data can be viewed on the website and the complete analysis of all phosphosites in the data can be downloaded as a CSV file.

## Data analysis file upload format
The uploaded file used for data analysis must be in the following format

-	tab or comma separated data saved as tsv, csv or txt format
-	X columns containing the following information in the following order.
Substrates. **UPDATE AS APPROPRIATE**

  1)	Control  
  2)	Condition  
  3)	P value  
  4)	CV


## Data sources
The data contained within the PhosphoQuest database is compiled from resources at Uniprot, PhophositePlus, BindingDb and… **UPDATE AS APPROPRIATE**.
Links to these resources are listed below:

https://www.uniprot.org

https://www.phosphosite.org/homeAction.action

https://www.bindingdb.org/bind/index.jsp

## Basic Software Specifications
PhosphoQuest is developed in Python 3.6+ using Flask and runs on Windows, Linux and Mac OS. The database is running in sqlite3. The web interface can be viewed in any modern browser; however, we recommend the latest versions of Chrome, Firefox and Edge to ensure correct page rendering.

## Software requirements to run the PhosphoQuest Server.
(ADD REQUIREMENTS HERE)

