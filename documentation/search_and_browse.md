# Browse and Search Script functions

## Search script overview

An overview of how the search scripts interact in the application is shown below.

![Search script interaction](***ADD PNG LINK***)

## Search script information
`routes.py` and `forms.py` within the `search` folder of the `PhosphoQuest_app` contain the Flask routes and Flask form class set up for display
of the search page on the web-app.

`Forms.py` sets up the search form with options for the database table to search (currently limited to *Kinases*, *Substrates* and *Inhibitors*, which information to search (*accession/ID* and *name*) and which type of search to perform (*like* or *exact*).

`routes.py` contains the Flask route `/search` which receives the user input from the forms, calls auzxillary functions and renders different templates depending on user input and query results. 

The `query_switch` function within `query_db.py` which is located within the `data_access` folder layer is called by the `routes.py` and handles the differing options and searches based on the user inputs from the form. The formats of the various outputs depending on the number of query results are also handled by functions within `query_db.py` before being passed back to `routes.py` for rendering on the template, `search_results.html` template.  

`search_results.html` is a generic template that is used to display many different types of search result outputs and is also used for displaying all of the browse result outputs. 

## Browse script overview
An overview of how the search scripts interact in the application is shown below.

![Browse script interaction](***ADD PNG LINK***)
