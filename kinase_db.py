from flask import Flask, render_template

# create instance of FLASK class. __name__ is name of module.
app = Flask(__name__)

# create route for home page works with / and /home page address
#uses home html template
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#route for browse page with browse template
@app.route("/browse")
def browse():
    return render_template('browse.html')

# if run from python directly run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
