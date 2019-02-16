from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# create instance of FLASK class. __name__ is name of module.
app = Flask(__name__)

# security for site secret key generated in python using secrets module
# token hex method
app.config['SECRET_KEY'] = '7302b128c277227526063af5c73ec426'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)

# import blueprints from package
#from PhosphoQuest_app.users.routes import users
from PhosphoQuest_app.main.routes import main
from PhosphoQuest_app.browse.routes import browse
from PhosphoQuest_app.search.routes import search
from PhosphoQuest_app.crunch.routes import crunch

# register blueprints with app
#app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(browse)
app.register_blueprint(search)
app.register_blueprint(crunch)

