from flask import Flask

# create instance of FLASK class. __name__ is name of module.
app = Flask(__name__)

# security for site secret key generated in python using secrets module
# token hex method
app.config['SECRET_KEY'] = '7302b128c277227526063af5c73ec426'

# CODE FOR USERS DATABASE FOR POSSIBLE USE IN FUTURE
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)

# import blueprints from package
#from PhosQuest_app.users.routes import users
from PhosQuest_app.main.routes import main
from PhosQuest_app.browse.routes import browse
from PhosQuest_app.search.routes import search
from PhosQuest_app.crunch.routes import crunch
from PhosQuest_app.errors.handlers import errors

# register blueprints with app
#app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(browse)
app.register_blueprint(search)
app.register_blueprint(crunch)
app.register_blueprint(errors)


