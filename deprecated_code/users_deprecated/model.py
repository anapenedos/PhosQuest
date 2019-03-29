##module for user model - user db import from package
from PhosQuest_app import db


class User(db.Model):
    """ Class for db model for email and passwords"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        #string print method
        return f"User('{self.email}')"