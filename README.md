# PhosphoQuest Application Readme

NB: After building this application we realised that there is a commerical product named PhosphoQuest, which is a Kinase ELISA. We would therefore need to change the name of this application prior to making this repository freely available and edit this in the code and documentation.

## Index

### General information for Repository Users
* [Website functionality - Basic overview](README.md#website-functionality---basic-overview)
* [Data sources](README.md#data-sources)
* [Data analysis](README.md#Data-analysis)
    * [File upload format](README.md#file-upload-format)
    * [General summary](README.md#general-summary)
    * [Output visuals](README.md#output-visuals)

### Information for Developers
* [Setting up the Database](README.md#setting-up-the-database)
* [Software Specifications](README.md#software-specifications)
* [Setting up the PhosphoQuest Application](README.md#setting-up-the-phosphoquest-application)
* [Python Package requirements](README.md#python-package-requirements)
* [Software architecture](README.md#software-architecture)

### Other information
* [About the developers](README.md#about-the-developers)
* [Areas for further development](README.md#areas-for-further-development)


## General information for Repository Users

### Website functionality - Basic overview
PhosphoQuest is a web application designed to enable users to search and browse a compiled database containing information about Human protein kinases, their substrates and inhibitors with related phosphosite information. 

The application also provides an area for users to upload a tsv or csv file of experimental mass-spectrometry data and receive outputs showing sites for which phosphorylation was significantly up- or down-regulated, and other useful analysis. The analysed data can be viewed on the website and the complete analysis of all phosphosites in the data can be downloaded as a CSV file.

### Data sources
Resources in this database (DB) were obtained from various sites. We thank everyone involved with maintaining, updating and keeping these data available and free to use for non-commercial purposes. 
The majority of the information on this website was obtained from, the superb online resource, [PhosphoSitePlus](https//www.phosphosite.org/).

Inhibitors information was obtained from [MRC Kinase Profiling Inhibitor Database](http://www.kinase-screen.mrc.ac.uk) and [BindingDB](https://www.bindingdb.org).

Additional information to popuplate the DB was obtained via API from [Uniprot](https://www.uniprot.org) and [PubChem](https://pubchem.ncbi.nlm.nih.gov/). Particular thanks to PubChem developers for providing the widget resources which are used on the inhibitor detail information pages of this website.

More information on DB setup can be found in the [database documentation](documentation/database.md).

### Data analysis
#### File upload format
The uploaded file used for data analysis (.tsv, .csv or .txt) should adhere to the following format:

**Column 1**: Substrate column with gene name and site. Note that non-phosphorylated peptides should also be in the format indicated i.e. gene name(None). However, the analysis tool can also handle substrate entries for non-phosphorylated peptides that are only gene names. 

**Column 2**: Mean intensity of Control replicate intensities. 

**Column 3**: Mean intensity of Treatment/Condition replicate intensities. 

**Column 4**: Fold change calculation: Treatment over the Control. Note: these should not be log2 fold calculations! 

**Column 5**: T-test P-values. Please use uncorrected values, as PhosphoQuest will implement correction for multiple-testing errors. 

**Column 6-7**: Coefficients of variation (CV's) for the Control and Treatment/Condition columns, respectively. PhosphoQuest can also handle data that doesn't have these column entries. 

#### General summary

The PhosphoQuest analysis tool is designed with phosphoproteomics data in mind - that is mass spectrometry data generated from enrichment experiments. Uploaded user data that conforms to the earlier specification is processed in a series of steps that fit into 3 broad categories. 

**1.** Tool checks for data format conformity and extracts data that has at least 1 quantitation event. The data is then further analysed and filtered to extract information on broad categories. For example substrate/sites reported in 1 or both conditions, with CVs <=25% and entries that are only phospho-sites to name a few.

**2.** User calculated p-values are corrected for multiple testing errors - Benjamini-Hochberg method implemented with a default permissable error rate of 0.05 applied. User data is also queried against the PhosphoQuest database to find kinases and substrates that map to each other. Further analysis extracts "Metrics" of the data.

**3.** Kinase and substrate/sites frequency analysis carried out. Relative kinase activity analysis, based on log2 fold change calculations in substrate/site(s), is also implemented.

These steps effectively build a user table with original upload information and the extra analysis appended.

#### Output visuals 
PhosphoQuest generates a number of visuals, that we hope will help you interpret and understand your data. These take the following form:

**Styled tables**: Your analysed, filtered and sorted data is uploaded in the form of a styled table. We have implemented visual cues such as super-imposed heatmaps and barplots to clarify the groupings in your data. Both the standard data and kinase activity analysis take this form.

**Volcano plot**: We can also visualise significantly differentially expressed hits by plotting a scatter of log2 fold changes vs the corrected p-value for each phospho-site.

**WordCouds and Frequency charts**: Representations of the frequency with which substrates/sites and their kinases appear in the data.  

**Summary Metrics**: Data is visualised in a series of piecharts, that aim to summarise distributions in a number of categories. For example, by taking the proportion of phospho-peptides detected in the whole data, we can determine the efficiency of your pull-down strategy.


## Information for Developers

### Setting up the Database
To set up the database, download data from [PhosphoSitePlus](https://www.phosphosite.org), [MRC Kinase Profiling Inhibitor Database](http://www.kinase-screen.mrc.ac.uk) and [BindingDB](https://www.bindingdb.org), introduce the new file locations in the `table_parsing.py` script found in the `data_import_scripts` directory and then run `db_setup.py`. More details about how the DB is structured and populated can be found in the [database documentation](documentation/database.md).

### Software Specifications
PhosphoQuest is developed in Python 3.6+ using Flask 1.0.2 for web functionality and runs on Windows, Linux and Mac OS. The DB is setup in SQLite3. The web interface can be viewed in any modern browser; however, we recommend the latest versions of Chrome, Firefox and Edge to ensure correct page rendering (minor differences are seen between browsers due to different handling of css).

Webpage styles are based on html5 with Bootstrap CSS 4.2.1 with local tweaks, jquery is used for tabs on results page.

DB functionality uses SQLite3 and Python SQLalchemy. 

Data analysis uses numpy, pandas and statsmodels. Output plots are rendered using plotly and matplotlib, with WordCloud to provide visual representations. 

### Python Package requirements
- Babel 2.6.0
- Click 7.0
- Flask 1.0.2
- Flask-Babel 0.12.2
- flask-table  0.5.0
- Flask-WTF  0.14.2
- itsdangerous  1.1.0
- Jinja2  2.10
- MarkupSafe  1.1.0
- numpy  1.15.4
- pandas  0.23.4
- plotly  3.7.0
- python-dateutil 2.7.5
- pytz  2018.9
- seaborn  0.9.0
- six  1.12.0
- SQLAlchemy  1.2.16
- statsmodels  0.9.0
- Werkzeug  0.14.1
- wordcloud  1.5.0
- WTForms  2.2.1
- xlrd  1.2.0

### Setting up the PhosphoQuest Application

All the PhosphoQuest web application packages are contained in the PhosphoQuest_app folder. 

Ensure that the DB location for the accompanying PhosphoQuest.db is `/database/PhosphoQuest.db` in the folder location outside of the `PhosphoQuest_app` folder. If a different database location is required, then it will be necessary to edit the path in the `db_sessions.py` script in the `data_access` folder within the `PhosphoQuest_app`.

After installation of all the requirements and set-up of the database run the `application.py` script (eg. `python3 application.py`) from the outer folder level. This will initiate the Flask application and server. Navigate to the IP address indicated in your terminal (e.g., `127.0.0.1:5000/`) in your browser to view the web application (run on local computer).

### Software architecture
The structure of the software in the Giardello repository consists of a `PhosphoQuest_app` folder containing subfolders corresponding to Flask Blueprints for routes `main`, `search`, `browse`, and `crunch`. The `static` folder contains images, the `main.css` local css file within a subfolder called `styles`, and a `userdata_temp` folder for temporary storage of user data and output files. the `templates` folder contains all the website html template files. The python scripts are broken into `service-scripts` containing python scripts used for user data analysis and `data_access` scripts containing functions for querying the PhosphoQuest DB.

Outside of the app folder `data_import_scripts` folder contains scripts used in the set up of the database. `application.py` is the python script used to initiate the PhosphoQuest application. 

The PhosphoQuest.db file should be located in a folder `database`, in the level outside `PhosphoQuest_app`.

Further information regarding the script functions is available in the following markdown documents and in comments in the scripts themselves:

* [Overview of PhosphoQuest Software structure](documentation/flask_application.md)
* [Detail on analysis script functions](documentation/user_data_analysis.md)
* [Detail on plotting script functions](documentation/plotting.md)
* [Detail on search and browse script functions](documentation/search_and_browse.md)
* [Detail on database setup](documentation/database.md)

## Other information
### About the developers
We are a group of part-time MSc Bioinformatics students at Queen Mary University of London, School of Biological and Chemical Sciences. This Web-Application was developed as the group project requirement of the course within a 12 week deadline and therefore, at this stage, the software will not be updated after 29/03/2019.

### Areas for further development
* Further categories added to browse and search functionality; 
* Update design of browse categories pages;
* Add links to DB disease information;
* Use url variables for passing browse and search variables back to query functions instead of string-split method;
* Utilise browser cookies for further functionality with user data upload;
* Add further functionality to upload page to show data analysis is happening (spinner or progress bar);
* Add user data analysis options (eg. selectable P-value or %CV cut offs);
* Consider adding option for users to be able to store data analysis in database for a short period of time;
* Curate kinase cellular location, protein family and disease data and break them down into several tables containing categories and sub-categories that could then be automatically be used for browse categories;
* Improve DB normalisation in general, for instance, by creating a join table containing all alternative gene names associated with a GenBank accession number, and associate substrate isotype accession numbers to a single substrate record;
* Produce a network diagram containing the top phosphorylated residues and related kinases to display in the user data analysis.
