from flask import flash, render_template, Blueprint, send_file
from PhosphoQuest_app.service_scripts import user_data_crunch
from PhosphoQuest_app.service_scripts import userdata_display
from werkzeug.utils import secure_filename
import traceback

from PhosphoQuest_app.crunch.forms import UploadForm
import os
crunch = Blueprint('crunch', __name__)


# route for upload page with file handling method
@crunch.route('/analysis',methods=['GET', 'POST'])
def analysis():
    """ Upload and analysis Route : run all analyses in crunch script.
    Produces all date dictionary, with datalist of dataframes for piecharts
    and further display
    all_data contains {'styn', 'sty', 'corrected_p','full_sty_sort':,
    'parsed_sty_sort','datalist'}

    datalist = [phos_enrich, AA_mod_res_freq, multi_phos_res_freq,
    prot_freq]"""
    form = UploadForm()

     #if form validates (correct file types) save file in temp dir
    if form.validate_on_submit():
        try:
            #get file from form and access filename
            f = form.data_file.data
            filename =  secure_filename(f.filename)
            #run all data crunch functions and create dictionary of results
            all_data = userdata_display.run_all(f)
            #create csv of all data for download
            csvdf= all_data['full_sty_sort']

            csv = userdata_display.create_csv(csvdf, filename)
            #selector for type of report (test version)
            if form.select.data == 'full':
                #output for full data
                table = all_data['full_sty_sort']
                table = table.to_html()

                flash(f'File {filename} successfully analysed', 'success')
                return render_template('results.html',
                            title='All results', table=table, csv=csv)

            else:
                #output for significant hits
                table = user_data_crunch.\
                         style_df(all_data['parsed_sty_sort'])

                flash(f'File {filename} successfully analysed', 'success')
                #temporary display of phos enrich
                phos_enrich = all_data['datalist'][0]
                phos_enrich=phos_enrich.to_html()
                return render_template('results.html',
                    title='All data', table=table, phos_enrich=phos_enrich,
                                       csv=csv)

        except Exception:
            #catch any file exception with traceback to help debugging
            flash(f'Error please try again ','danger')
            return render_template('upload.html', form=form, report='upload')

    return render_template('upload.html', form=form, report='upload')


@crunch.route('/download_analysis/<csv>',methods=['GET', 'POST'])
def download_analysis(csv):
    """App route to download data analysis csv."""
    #form required only for exception when upload rendered
    form = UploadForm()

    if not csv:
       return "No file"

    else:
        tempdir = os.path.join('user_data', 'temp')
        file = os.path.join(tempdir, csv)

        return send_file(file,
                     mimetype='text/csv',
                     attachment_filename=csv,
                     as_attachment=True)