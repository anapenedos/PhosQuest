"""scripts to format subsets of crunched data for display"""
from service_scripts import ud_crunch
import pandas as pd

def run_all(file, filename):
    """Function to run all analyses"""
    styn, sty = ud_crunch.create_filtered_dfs(file)

    corrected_p = ud_crunch.correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort =\
        ud_crunch.table_sort_parse(corrected_p)

    #collate extracted data as datalist
    a,b,c,d = ud_crunch.data_extract(full_sty_sort, styn)

    datalist = [a,b,c,d]

    all_html = full_sty_sort.to_html()
    sig_html = parsed_sty_sort.to_html()


    #This can change depending on what is needed for display in route
    all_data = {'styn':styn, 'sty':sty, 'corrected_p':corrected_p,
        ' full_sty_sort': full_sty_sort, 'parsed_sty_sort':parsed_sty_sort,
        'datalist':datalist, 'all_html':all_html,'sig_html':sig_html}


    #These files are currently just being saved to a directory
    user_data_crunch.heat_map(full_sty_sort, f"{filename}_full")

    user_data_crunch.heat_map(parsed_sty_sort, f"{filename}_parsed")

    #return all outputs and datalist html tables
    return(all_data)


#might come later if we decide to have downloadable csv from user area
def export_to_csv(full_sty_sort,parsed_sty_sort):

    full_sty_sort.to_csv("../user_data/full_sorted_hits.csv")

    parsed_sty_sort.to_csv("../user_data/significant_sorted_hits.csv")
    create_filtered_dfs(datafile)



