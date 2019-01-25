from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create instance of FLASK class. __name__ is name of module.
app = Flask(__name__)

# security for site secret key generated in python using secrets module
# token hex method
app.config['SECRET_KEY'] = '7302b128c277227526063af5c73ec426'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

#import routes from package
from kinase_db_app import routes