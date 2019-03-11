"""scripts to format subsets of crunched data for display"""
from PhosphoQuest_app.service_scripts import user_data_crunch
from datetime import datetime
import os

def run_all(df):

    """Function to run all crunch analyses on dataframe"""
    # run data crunch analyses
    styno, sty = user_data_crunch.create_filtered_dfs(df)

    corrected_p = user_data_crunch.correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort, db_kin_dict =\
        user_data_crunch.table_sort_parse(corrected_p)

    #run volcano plot
    volcano = user_data_crunch.user_data_volcano_plot(full_sty_sort)


    # collate extracted data as datalist
    phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq =\
                    user_data_crunch.data_extract(full_sty_sort, styno)

    datalist = [phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq]


    # This can change depending on what is needed for display in route
    all_data = {'styno':styno, 'sty':sty, 'corrected_p':corrected_p,
        'full_sty_sort': full_sty_sort, 'parsed_sty_sort':parsed_sty_sort,
        'datalist':datalist, 'volcano':volcano}

    """ Upload and analysis Route : run all analyses in crunch script.
    Produces all date dictionary, with datalist of dataframes for piecharts
    and further display and html of volcano plot.
    all_data contains {'styno', 'sty', 'corrected_p','full_sty_sort':,
    'parsed_sty_sort','datalist'}

    datalist = [phos_enrich, AA_mod_res_freq, multi_phos_res_freq,
    prot_freq]"""
    #return all outputs and datalist html tables
    return(all_data)


def create_csv(dataframe, filename):
    """ function to create full  dataframe as csv"""
    tempdir = os.path.join("PhosphoQuest_app/user_data", 'temp')
    time = str(datetime.now()) # get time now
    # get date last 3 digits (milliseconds) as "unique" no for download
    id = time[-3:]
    date= time[:10]
    outname = f"{date}-{filename}_analysed_id{id}.csv"
    #SAVE FILE
    dataframe.to_csv(os.path.join(tempdir,outname))

    # clean up old files >1 day
    oldfiles = [name for name in os.listdir(tempdir) if\
          os.path.isfile(os.path.join(tempdir, name))]
    # get date from file name
    for oldfile in oldfiles:
        date = oldfile[:10]
        # ignore tempfolder file
        if date != 'temp_folde':
            date = datetime.strptime(date, '%Y-%m-%d')
            if abs((datetime.now() - date).days) >1:
                #remove file if more than 1 day old
                os.remove(os.path.join(tempdir,oldfile))
                print(oldfile + "_removed")
    return outname

def volcano_html(html_file,filename):
    t