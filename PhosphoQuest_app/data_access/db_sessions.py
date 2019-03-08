import os
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.interfaces import PoolListener


def session_maker(db_path=os.path.join('database', 'PhosphoQuest.db')):
    """
    Produces a session maker object for standard database query sessions.

    :param db_path: system path to relevant DB (str)
    :return: DB sesseion maker object (sqlalchemy sessionmaker)
    """
    engine = create_engine('sqlite:///' + db_path, echo=False)
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    return DBSession


def print_sql_session_maker(db_path=os.path.join(
    'database', 'PhosphoQuest.db')):
    """
    Produces a session maker object for database query sessions where sql
    statements are printed to console.

    :param db_path: system path to relevant DB (str)
    :return: DB sesseion maker object (sqlalchemy sessionmaker)
    """
    engine = create_engine('sqlite:///' + db_path, echo=True)
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    return DBSession


class MyListener(PoolListener):
    """
    Class defining session execution in SQLite. Allows OS management of
    writing to disk operations, speeding up imports.
    """
    def connect(self, dbapi_con, con_record):
        dbapi_con.execute('pragma journal_mode=OFF')
        dbapi_con.execute('PRAGMA synchronous=OFF')
        dbapi_con.execute('PRAGMA cache_size=100000')


def import_session_maker(db_path=os.path.join('database', 'PhosphoQuest.db')):
    """
    Produces a session maker object for database import sessions, where write
    operations are managed by OS.

    :param db_path: system path to relevant DB (str)
    :return: DB session maker object (sqlalchemy sessionmaker)
    """
    # Create engine that stores data to database\<file_name>.db
    # defines engine as SQLite, uses listeners to implement faster import
    # (record writing to disk is managed by the OS and hence can occur
    # simultaneously with data processing
    engine = create_engine('sqlite:///' + db_path, echo=False,
                           listeners=[MyListener()])
    # Bind the engine to the metadata of the base class so that the
    # classes can be accessed through a DBSession instance
    Base.metadata.bind = engine
    # DB session to connect to DB and keep any changes in a "staging zone"
    DBSession = sessionmaker(bind=engine)
    return DBSession


def pandas_sql_session_maker(db_path=os.path.join('database',
                                                  'PhosphoQuest.db')):
    """
    Produces a session maker object to use when visualising sqlalchemy with a
    pandas data frame.

    :param db_path: system path to relevant DB (str)
    :return: DB session maker object (sqlalchemy sessionmaker)
    """
    # Define instance of engine which represents interface to the database.
    engine = create_engine('sqlite:///' + db_path, echo=False)
    # Define session class object - ORM "handle" to the data-base.
    DBSession = sessionmaker()
    # Connect engine to the Session object.
    DBSession.configure(bind=engine)
    return DBSession


def create_sqlsession(existing_maker=None,
                       session_type='standard',
                       db_path=os.path.join('database', 'PhosphoQuest.db')):
    """
    Returns a sqlalchemy session object of the type specified.

    :param existing_maker: existing DB maker object (sqlalchemy sessionmaker)
                           default is None
    :param session_type: type of session desired (str)
                         'standard' normal DB query
                         'import' optimises DB connection for large data import
                         'pandas_sql' allows visualising sqlalchemy with pandas
                         'print_sql' prints sqlite statements to screen
                         default is 'standard'
    :param db_path: system path to relevant DB (str)
                    default is 'PhosphoQuest.db' DB in database folder
    :return: DB session object (sqlalchemy session)
    """
    if not existing_maker:
        maker = {'standard': session_maker(db_path),
                 'import': import_session_maker(db_path),
                 'print_sql': print_sql_session_maker(db_path),
                 'pandas_sql': pandas_sql_session_maker(db_path)}
        DBSession = maker[session_type]
    else:
        DBSession = existing_maker
    # open a SQLite session
    session = DBSession()
    return session