# run app from package in debug mode
from PhosphoQuest_app import app
import pandas as pd


if __name__ == '__main__':
    app.run(debug=True)


pd.options.mode.chained_assignment = None
