"""scripts to format subsets of crunched data for display"""
from PhosphoQuest_app.service_scripts import user_data_crunch, plotting
from datetime import datetime
import os


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
    subs_sites_word_str, \
    kinase_activities = \
        user_data_crunch.kinase_analysis(db_kin_dict, parsed_sty_sort)

        # collate extracted data
    phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq =\
                    user_data_crunch.data_extract(full_sty_sort, styno)

    # Create dictionary of needed output variables for returning from function
    all_data = {
        #styno':styno, 'sty':sty, 'corrected_p':corrected_p,
        'full_sty_sort': full_sty_sort, 'parsed_sty_sort':parsed_sty_sort,
        'phos_enrich':phos_enrich, 'AA_mod_res_freq':AA_mod_res_freq,
        'multi_phos_res_freq':multi_phos_res_freq, 'prot_freq':prot_freq,
        'kinase_target_freq':kinase_target_freq, 'kinase_freq':kinase_freq,
        'kin_word_str':kin_word_str, 'subs_sites_word_str':subs_sites_word_str,
        'kinase_activities':kinase_activities
        }
    #return all outputs and datalist html tables
    return(all_data)

def plot_all(all_data):
    """
    Function to run all plotting and wordcloud functions from plotting.py
    :param all_data: dict, dictionary of all analysis outputs
    :return: dict, dictionary of all plot variables
    """

    # Analysis tab 1 display - Styled table of significant hits and kinase
    # activity

    table = plotting.style_df(all_data['parsed_sty_sort'],
                 all_data['kinase_activities'])

    # Tab 2 run volcano plot on full_sty_sort dataframe
    volcano = plotting.user_data_volcano_plot(all_data['full_sty_sort'])

    # Tab 3 wordcloud frequency charts
    # create wordclouds and frequency barcharts and pass filenames to template
    kin_wcloud,\
    subs_sites_wcloud,\
    kin_freq,\
    kin_target_freq = plotting.wordcloud_freq_charts(all_data['kin_word_str'],
                              all_data['subs_sites_word_str'],
                              all_data['kinase_freq'],
                              all_data['kinase_target_freq'])

    # Tab 4  Summary pie charts

    phos_enrich_pie = plotting.pie_chart(all_data['phos_enrich'],'Total',
                           'phos_enrich_pie', 2)


    multi_phos_res_freq_pie = \
        plotting.pie_chart(all_data['multi_phos_res_freq'],'Frequency',
                           'multi_phos_res_freq_pie')

    AA_mod_res_freq_pie = plotting.pie_chart(all_data['AA_mod_res_freq'],
                                'Total number with phospho',
                                                      'AA_mod_res_freq_pie')



    all_plots= {
        'table':table, 'volcano':volcano, 'kin_wcloud':kin_wcloud,
        'subs_sites_wcloud':subs_sites_wcloud, 'kin_freq':kin_freq,
        'kin_target_freq':kin_target_freq, 'phos_enrich_pie':phos_enrich_pie,
        'multi_phos_res_freq_pie':multi_phos_res_freq_pie,
        'AA_mod_res_freq_pie':AA_mod_res_freq_pie
        }
    return all_plots

def create_csv(dataframe, filename):
    """
    function to create full  dataframe as csv
    :param dataframe: pd.dataframe
    :param filename: string
    :return: string of full filename including file extension

    """
    tempdir = os.path.join('PhosphoQuest_app','static', 'userdata_temp')

    #capture input file name for output csv
    text = f"{filename}_analysed"

    #run create userfilename function to get used specific filename
    outname = plotting.create_userfilename(text, 'csv')

    #SAVE FILE
    dataframe.to_csv(os.path.join(tempdir,outname))

    # clean up old files in userdata_temp folder >1 day old
    oldfiles = [name for name in os.listdir(tempdir) if\
          os.path.isfile(os.path.join(tempdir, name))]

    # get date from file name
    for oldfile in oldfiles:
        date = oldfile[:10]
        # ignore tempfolder file

        try:
            # reformat to datetime object
            date = datetime.strptime(date, '%Y-%m-%d')
            if abs((datetime.now() - date).days) >1:
                #remove file if more than 1 day old
                os.remove(os.path.join(tempdir,oldfile))
                print(oldfile + "_removed")
        except ValueError: # if format not compatible with date ignore
            pass

    return outname
