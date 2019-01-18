from flask import Flask, render_template

# create instance of FLASK class. __name__ is name of module.
app = Flask(__name__)

# Set up list of browse data (Just testing!!) could be imported as a list of dicts (or python object??)
browse_data = [
    {'accession':'Q16836',
        'name': 'Hydroxyacyl-coenzyme A dehydrogenase',
        'Molecular_Function':'NAD+_binding',
        'Cellular_component':'cytosol',
        'Biological_Process': 'Fatty acid beta oxidation',
        'link':'https://www.uniprot.org/uniprot/Q16836'},
    {'accession': 'P35914',
        'name': 'Hydroxymethylglutaryl-CoA lyase',
        'Molecular_Function': 'carboxylic acid binding',
        'Cellular_component': 'cytosol',
        'Biological_Process': 'ketone body biosynthetic process',
         'link': 'https://www.uniprot.org/uniprot/P35914'}]


# create route for home page works with / and /home page address
# uses home html template
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# route for browse page with browse template
@app.route("/browse")
def browse():
    # render template with browse data and title for browse page
    return render_template('browse.html', browse_data=browse_data, title="BROWSE")


# if run from python directly run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
