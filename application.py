# run app from package in debug mode
from PhosQuest_app import app
import pandas as pd


if __name__ == '__main__':
    app.run(debug=False)

# setting up for Amazon Elastic Beanstalk to be able to find the application
application = app

pd.options.mode.chained_assignment = None
