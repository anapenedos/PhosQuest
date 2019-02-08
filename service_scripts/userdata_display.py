"""scripts to format subsets of crunched data for display"""
from service_scripts import user_data_crunch
import pandas as pd

def run_all(file, filename):
    """Function to run all analyses"""
    styn, sty = user_data_crunch.create_filtered_dfs(file)

    corrected_p = user_data_crunch.correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort =\
        user_data_crunch.table_sort_parse(corrected_p)

    datalist = [user_data_crunch.data_extract(full_sty_sort, styn)]



    all_data = {
        'styn':styn, 'sty':sty, 'corrected_p':corrected_p,
        ' full_sty_sort': full_sty_sort, 'parsed_sty_sort':parsed_sty_sort,
        'datalist':datalist
    }


    #These files are currently just being saved to a directory
    heat_map(full_sty_sort, f"{filename}_full")

    heat_map(parsed_sty_sort, f"{filename}_parsed")
    #return all outputs
    return(all_data)


#might come later if we decide to have downloadable csv from user area
def export_to_csv(full_sty_sort,parsed_sty_sort):

    full_sty_sort.to_csv("../user_data/full_sorted_hits.csv")

    parsed_sty_sort.to_csv("../user_data/significant_sorted_hits.csv")
    create_filtered_dfs(datafile)



