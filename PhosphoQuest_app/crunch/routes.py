from flask import flash, render_template, Blueprint, send_file
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

     #if form validates (correct file types) save file in temp dir
    if form.validate_on_submit():
        try:
            #get file from form and access filename
            f = form.data_file.data
            filename =  secure_filename(f.filename)

            #check file and return error or dataframe
            check_var = user_data_crunch.user_data_check(f)


            if type(check_var) != str: # if not string run analysis

                #run all data crunch functions and create dictionary of results
                all_data = userdata_display.run_all(check_var)

                #create csv of all data for download
                csvdf = all_data['full_sty_sort']

                csv = userdata_display.create_csv(csvdf, filename)

                #output for significant hits
                table = user_data_crunch.\
                         style_df(all_data['parsed_sty_sort'],
                                  all_data['kinase_activities'])

                volcano = all_data['volcano']

                flash(f'File {filename} successfully analysed', 'success')

                #temporary display of phos enrich
                phos_enrich = all_data['datalist'][0]
                phos_enrich=phos_enrich.to_html()


                return render_template('results.html',
                    title='Analysis', table=table, phos_enrich=phos_enrich,
                                      volcano=volcano, csv=csv)

            else: # if string show user error
                flash(check_var, 'danger')
                return render_template('upload.html', form=form,
                                       report='upload')

        except Exception as ex:
            # catch any file exception with error shown to help debugging
            flash('An error occurred please try again','danger')
            flash(ex, 'danger')
            return render_template('file_error')

    return render_template('upload.html', form=form, report='upload')


@crunch.route('/download_analysis/<csv>',methods=['GET', 'POST'])
def download_analysis(csv):
    """App route to download data analysis csv."""
    try:
        tempdir = os.path.join('user_data', 'temp')
        file = os.path.join(tempdir, csv)

        return send_file(file,
                     mimetype='text/csv',
                     attachment_filename=csv,
                     as_attachment=True)
    except:
        #TODO update to file handling error page
        return render_template('404_error.html')

@crunch.route('/file_error')
def file_error():
    """File not found error template route"""
    return render_template('file_error.html')