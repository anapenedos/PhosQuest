# Functions for import of API data

# standard library imports
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
import pandas as pd
import urllib.request
import urllib.parse

# project-specific imports
from data_access.sqlalchemy_declarative import Base

# =========================================================================== #


def get_uniprot_api_data(class_name):
    # get the name of the primary key attribute in the class's corresponding
    # table
    key_attr = inspect(class_name).primary_key[0].name

    # get a list of the key values present in the table
    # Create engine that stores data to database\<file_name>.db
    db_path = os.path.join('database', 'PhosphoQuest.db')
    # defines engine as SQLite, uses listeners to implement faster import
    # (record writing to disk is managed by the OS and hence can occur
    # simultaneously with data processing
    engine = create_engine('sqlite:///' + db_path, echo=False)
    # Bind the engine to the metadata of the base class so that the
    # classes can be accessed through a DBSession instance
    Base.metadata.bind = engine
    # DB session to connect to DB and keep any changes in a "staging zone"
    DBSession = sessionmaker(bind=engine)
    # open a SQLite session
    session = DBSession()

    # list of the value for the key field for all records [('val1',),...]
    records = session.query(getattr(class_name, key_attr)).all()

    #close the session
    session.close()

    # convert into list of str ['val1', ...]
    keys_list = [val[0] for val in records]
    # convert list into Uniprot query format 'val1 val2'
    query_str = ' '.join(keys_list)

    # Get the corresponding data
    # The default base URL.
    url = 'https://www.uniprot.org/uploadlists/'

    # Parameters for UniProt API site, selecting specific qualifiers using the
    # api_query_accession variable from the accession list function.
    params = {
        'from': 'ACC',
        'to': 'ACC',
        'format': 'tab',
        'columns': 'id,protein names,comment(SUBCELLULAR LOCATION),families',
        'query': query_str
    }

    # Takes the parameters and encodes it as it should be in the URL
    # (e.g. %20 = 'a space').
    data = urllib.parse.urlencode(params)

    # Changes it to a type of encoding, e.g. bytes.
    data = data.encode('utf-8')

    # Requests the URL and and data (which has already been encoded above).
    request = urllib.request.Request(url, data)

    # Opens the URL with paramters.
    response = urllib.request.urlopen(request)

    # Places the data into a dataframe.
    df = pd.read_table(response)

    # Converts a replicate Subcellular location column in string format.
    df['Subcellular location55'] = df['Subcellular location [CC]'].astype(str)

    # Specfiically extracts the Subcellular location information (and nothing
    # else) from the orignal column and places is /
    # within the new Subcellular loation columns.
    df['Subcellular location55'] = df['Subcellular location55'].str.extract(
        '(?<=SUBCELLULAR LOCATION: )(.*?)(?={)', expand=True)

    # extract single protein name
    df['Protein name'] = df['Protein names'].astype(str)
    df['Protein name'] = df['Protein name'].str.extract('(.*?) \(.*',
                                                        expand=True)
    return df