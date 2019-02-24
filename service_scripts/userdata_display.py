"""scripts to format subsets of crunched data for display"""
from service_scripts import user_data_crunch


def run_all(file):

    """Function to run all crunch analyses"""
    styn, sty = user_data_crunch.create_filtered_dfs(file)

    corrected_p = user_data_crunch.correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort =\
        user_data_crunch.table_sort_parse(corrected_p)


    #collate extracted data as datalist
    phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq =\
                    user_data_crunch.data_extract(full_sty_sort, styn)

    datalist = [phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq]

        #This can change depending on what is needed for display in route
    all_data = {'styn':styn, 'sty':sty, 'corrected_p':corrected_p,
        'full_sty_sort': full_sty_sort, 'parsed_sty_sort':parsed_sty_sort,
        'datalist':datalist}

    """ Upload and analysis Route : run all analyses in crunch script.
    Produces all date dictionary, with datalist of dataframes for piecharts
    and further display
    all_data contains {'styn', 'sty', 'corrected_p','full_sty_sort':,
    'parsed_sty_sort','datalist'}

    datalist = [phos_enrich, AA_mod_res_freq, multi_phos_res_freq,
    prot_freq]"""
    #return all outputs and datalist html tables
    return(all_data)


