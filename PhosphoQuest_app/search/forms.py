from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField



class SearchForm(FlaskForm):
    """Search form with selectors"""
    search = StringField('Enter Search text')
    #Dropdown selector for exact or like match
    options= [('like', 'similar matches'),('exact', 'exact matches')]
    select = SelectField('Choose search type: ', choices=options)

    #radio button selector for table to search
    criteria =[
        ('kinase', 'Kinases'), ('substrate','Substrates'),
        ('inhibitor','Inhibitors')]

    table = RadioField('Search by: ', choices=criteria, default='kinase')

    fields = [('acc_no', 'Accession or ID'), ('name', 'Name')]

    option = RadioField('Search in: ', choices=fields, default='acc_no')

    submit = SubmitField("Search")
