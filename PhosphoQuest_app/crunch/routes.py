from flask import flash, render_template, Blueprint, send_file, session
from PhosphoQuest_app.service_scripts import user_data_crunch
from PhosphoQuest_app.service_scripts import userdata_display
from werkzeug.utils import secure_filename

from PhosphoQuest_app.crunch.forms import UploadForm
import os
crunch = Blueprint('crunch', __name__)


# route for upload page with file handling method
@crunch.route('/analysis',methods=['GET', 'POST'])
def analysis():
    """ Upload and analysis Route : run all analyses in crunch script.
    Produces all date dictionary, with datalist of dataframes for piecharts
    and further display
    all_data contains {'styno', 'sty', 'corrected_p','full_sty_sort':,
    'parsed_sty_sort','datalist','volcano', 'kinase_activities'}

    datalist = [phos_enrich, AA_mod_res_freq, multi_phos_res_freq,
    prot_freq]"""
    form = UploadForm()

     #if form validates (correct file types) save file in userdata_temp dir
    if form.validate_on_submit():
        # try:
        # get file from form and access filename
        f = form.data_file.data
        filename = secure_filename(f.filename)
        #remove file extension - string of name (friendly for reuse later)
        filename = os.path.splitext(filename)[0]
        # replace any spaces in filename input text with underscores
        filename = filename.replace(" ", "_")
        #create session cookie for filename
        session['file']= filename


        #check file and return error string or dataframe
        check_var = user_data_crunch.user_data_check(f)


        if type(check_var) != str: # if not string run analysis

            #run all data crunch functions and create dictionary of results
            all_data = userdata_display.run_all(check_var)

            # run all plotting functions and create dictionary of results
            plots = userdata_display.plot_all(all_data)

            # create csv of all data for download
            csvdf = all_data['full_sty_sort']
            csv = userdata_display.create_csv(csvdf)

            flash(f'File {filename} successfully analysed', 'success')
            return render_template('results.html',
                title='Analysis', plots=plots, csv=csv)

        else: # if string show user error
            flash(check_var, 'danger')
            return render_template('upload.html', form=form,
                                   report='upload')

        # except Exception as ex:
        #     # catch any file exception with error shown to help debugging
        #     flash('An error occurred please try again','danger')
        #     flash(ex, 'danger')
        #     return render_template('file_error.html')

    return render_template('upload.html', form=form, report='upload')


@crunch.route('/download_analysis/<csv>',methods=['GET', 'POST'])
def download_analysis(csv):
    """App route to download data analysis csv."""
    try:
        tempdir = os.path.join('static', 'userdata_temp')
        file = os.path.join(tempdir, csv)

        return send_file(file,
                     mimetype='text/csv',
                     attachment_filename=csv,
                     as_attachment=True)
    except:
        return render_template('file_error.html')

@crunch.route('/file_error')
def file_error():
    """File not found error template route"""
    return render_template('file_error.html')