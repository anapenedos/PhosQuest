# Browse and Search Script functions

## Search script overview

An overview of how the search scripts interact in the application is shown below.

![Search script interaction](***ADD PNG LINK***)

## Search script information
`routes.py` and `forms.py` within the `search` folder of the `PhosphoQuest_app` contain the Flask routes and Flask form class set up for display of the search page on the web-app.

`Forms.py` sets up the search form with options for the database table to search (currently limited to *Kinases*, *Substrates* and *Inhibitors*, which information to search (*accession/ID* and *name*) and which type of search to perform (*like* or *exact*).

`routes.py` contains the Flask route `/search` which receives the user input from the forms, calls auxillary functions from `data_access/query_db` and renders different templates depending on user input and query results. 

The `query_switch` function within `query_db.py` which is located within the `data_access` folder layer is called by the `routes.py` and handles the differing options and searches based on the user inputs from the form. The formats of the various outputs depending on the number of query results are also handled by functions within `query_db.py` before being passed back to `routes.py` for rendering on the template, `search_results.html` template.  

`search_results.html` is a generic template that is used to display many different types of search result outputs and is also used for displaying all of the browse result outputs. 

## Browse script overview
An overview of how the search scripts interact in the application is shown below.

![Browse script interaction](***ADD PNG LINK***)

`routes.py` within the `browse` folder of the `PhosphoQuest_app` contain the Flask routes for display of the various browse pages on the web-app.

The routes `browse_main` and `browse_cat`, render pages of browse category buttons. For some categories there is only one level of browse buttons to click (eg. inhibitors where the only browse option at present is to browse all inhibitors), for others there are several levels of buttons to click, eg *Kinases*, where they can be browsed by categories eg. *Kinase Family*, and then sub-categories eg.*Alpha-type protein kinase*. The categories *Kinase family* and *Kinase cellular location* are called from a dictionary of entries curated from the PhosphoQuest.db field for the respecive type. However the subcategory *Substrate-Chromosome location* is obtained from a database query for all chromosome locations and then parsed using a regular expression to show only distinct chromosome number (or X/Y) and p or q arms, eg (12p) to reduce the number of categories for adding to the browse buttons.

Clicking any of the final level category or subcategory buttons triggers a "like" query run from the function `searchlike()` in `data_access/query_db`

The `routes.py` functions deal with handling the different browse categories button display pages that are presented, and calls various functions from the `browse_queries.py` script wihtin the `data access` folder in order to do so. The routes described below handle the various different output types from the browse functions.

`browse_table` renders pages for tabular display of browse query results. The tables contain a *Detail* field which then links to the individual record information for each result item. 

The various `browse_XXXdetail` routes all perform queries and render pages for detail view of an individual item with tables of related information (eg. One kinase record with corresponding tables of related phosphosites and inhibitors). 

All results from the browse queries are displayed using the generic `search_results.html` template which can handle multiple different types of outputs. 
