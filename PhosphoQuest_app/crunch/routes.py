from flask import flash, render_template, Blueprint
from service_scripts import userdata_display, user_data_crunch
from werkzeug.utils import secure_filename
import traceback
from PhosphoQuest_app.crunch.forms import UploadForm

crunch = Blueprint('crunch', __name__)


# route for upload page with file handling method
@crunch.route('/analysis',methods=['GET', 'POST'])
def analysis():
    """Create upload and analysis route"""
    form = UploadForm()
     #if form validates (correct file types) save file in temp dir
    if form.validate_on_submit():
        try:
            f = form.data_file.data
            filename =  secure_filename(f.filename)
            #run all analyses.
            all_data = userdata_display.run_all(f)
            #selector for type of report (test version)
            if form.select.data == 'full':
                table = user_data_crunch.style_df(all_data['full_sty_sort'])
                # temporary test display bokeh df
                #table = userdata_display.bokeh_df(all_data['full_sty_sort']))

                flash(f'File {filename} successfully analysed', 'success')
                return render_template('results.html',
                            title='All results',
                                    table=table )

            else:

                table = user_data_crunch.\
                         style_df(all_data['parsed_sty_sort'])

                flash(f'File {filename} successfully analysed', 'success')

                return render_template('results.html',
                    title='All data', table=table)

        except Exception:
            print(traceback.format_exc())
            flash(f'Error please try again ','danger')
            return render_template('upload.html', form=form, report='upload')

    return render_template('upload.html', form=form, report='upload')


