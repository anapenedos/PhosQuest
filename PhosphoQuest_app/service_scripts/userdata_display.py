"""scripts to format subsets of crunched data for display"""
from PhosphoQuest_app.service_scripts import user_data_crunch
from datetime import datetime
from flask import session
import os


def create_userfilename(text, extension):
    """
    Function to create temp user id and store in session cookie
    and use to create unique file names for user-data incorporating date
    for cleanup purposes
    :param text: filename string eg: "plot", " analysed_data"
    :param extension: file extension to add (as string) eg 'csv'
    :return: full filename (string) for passing to os functions etc.
    """
    # get date time now and convert to string
    time = str(datetime.now())
    date = time[:10]

    # if session cookie already exists use date and existing id
    if 'id' in session:
        id = session['id']
        outname = f"{date}_{id}_{text}.{extension}"
        return outname

    # create user id cookie if not already in session
    else:
        # get date last 4 digits (milliseconds) as "unique" no for download
        id = "id" + time[-4:]
        # store cookie for reuse on other files
        session['id'] = id
        #use created id in filename
        outname = f"{date}_{id}_{text}.{extension}"
        return outname


def run_all(df):

    """Function to run all crunch analyses on dataframe"""
    # run data crunch analyses
    styno, sty = user_data_crunch.create_filtered_dfs(df)

    corrected_p = user_data_crunch.correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort, db_kin_dict =\
        user_data_crunch.table_sort_parse(corrected_p)

    # run kinase analysis
    kinase_target_freq, \
    kinase_freq, \
    kin_word_str, \
    subs_sites_word_str,\
    kinase_activities = \
        user_data_crunch.kinase_analysis(db_kin_dict, parsed_sty_sort)

    # run volcano plot
    volcano = user_data_crunch.user_data_volcano_plot(full_sty_sort)

    # collate extracted data as datalist
    phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq =\
                    user_data_crunch.data_extract(full_sty_sort, styno)

    datalist = [phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq]


    # Create dictionary of ouput varibles for returning from function
    all_data = {'styno':styno, 'sty':sty, 'corrected_p':corrected_p,
        'full_sty_sort': full_sty_sort, 'parsed_sty_sort':parsed_sty_sort,
        'datalist':datalist, 'volcano':volcano,
        'kinase_activities':kinase_activities}

    #return all outputs and datalist html tables
    return(all_data)


def create_csv(dataframe, filename):
    """
    function to create full  dataframe as csv
    :param dataframe: pd.dataframe
    :param filename: string
    :return: string of full filename including file extension

    """
    tempdir = os.path.join("PhosphoQuest_app/user_data", 'temp')

    #capture input file name for output csv
    text = f"{filename}_analysed"

    #run create userfilename function to get used specific filename
    outname = create_userfilename(text, 'csv')

    #SAVE FILE
    dataframe.to_csv(os.path.join(tempdir,outname))

    # clean up old files in temp folder >1 day old
    oldfiles = [name for name in os.listdir(tempdir) if\
          os.path.isfile(os.path.join(tempdir, name))]
    # get date from file name
    for oldfile in oldfiles:
        date = oldfile[:10]
        # ignore tempfolder file
        if date != 'temp_folde':
            #reformat to datetime object
            date = datetime.strptime(date, '%Y-%m-%d')
            if abs((datetime.now() - date).days) >1:
                #remove file if more than 1 day old
                os.remove(os.path.join(tempdir,oldfile))
                print(oldfile + "_removed")
    return outname
