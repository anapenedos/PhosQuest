### Plotting script. 

# --------------------------------------------------------------------------- #

### Import packages into environment.
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from flask import session
from datetime import datetime
import random
import os

# project imports
from PhosphoQuest_app.service_scripts.user_data_crunch import user_data_check,\
    create_filtered_dfs, correct_pvalue, table_sort_parse, data_extract, \
    kinase_analysis

#Define temporary directory path for output files
tempdir = os.path.join("PhosphoQuest_app","static", 'userdata_temp')


def create_userfilename(text, extension):
    """
    Function to create userdata_temp user id and store in session cookie
    and use to create unique file names for user-data incorporating date
    for cleanup purposes
    :param text: filename string eg: "plot", " analysed_data"
    :param extension: file extension to add (as string) eg 'csv'
    :return: full filename (string) for passing to os functions etc.
    """
    # get date time now and convert to string
    time = str(datetime.now())
    date = time[:10]

    # if session cookie already exists use date and existing id and name of
    # input file for output files

    if 'id' in session and 'file' in session:
        id = session['id']
        file = session['file']
        outname = f"{date}_{file}_{id}_{text}.{extension}"
        return outname

    # create user id  and file cookie if not already in session
    else:
        # get date last 4 digits (milliseconds) as "unique" no for download
        id = "id" + time[-3:]
            #use created id in filename
        outname = f"{date}_{id}_{text}.{extension}"
        return outname


def read_html_to_variable(file):
    """
    Function to open savedfile and read lines into variable
    :param file: string (path of file)
    :return: string
    """
    with open(file,'r') as f:
        outvar = f.read()

    return outvar


def pie_chart(df, header, name, removed=None):
    """
    Function to create piechart from dataframe with header of column for data
    and name string to add to file name string eg "mod_residue"
    :param df: pd.dataframe
    :param header:string
    :param name:string - name of pie chart eg "modified_residues"
    :param removed: int item index to remove from list (default none)
    :return: string - filename
    """
    # Import the row heading data as object.
    label0 = pd.Series(df.index)
    # Place them into a series (not as objects).
    labels = list(label0)


    # Import the specific values from the dataframe as a list.
    values = df[header].tolist()
    if removed != None:
        values.pop(removed)

    # Set core pie.
    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+value', textinfo='percent',
                   textfont=dict(size=20),
                   marker=dict(line=dict(color='#000000', width=2))
                   )

    # Define trace as data.
    data = [trace]
    filename = create_userfilename(name, 'html')
    outfile = os.path.join(tempdir,filename)

    # Plot the data in html format.
    plot(data, filename=outfile, auto_open=False)
    #return filename for adding to html template

    html = read_html_to_variable(outfile)
    return html
# # --------------------------------------------------------------------------- #
# ### Pie chart for phos_enrich.
#
# # Example data
# # labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
# # values = [4500,2500,1053,500]
#
# # Import the row heading data as object.
# label0 = pd.Series(phos_enrich.index)
# # Place them into a series (not as objects).
# labels = list(label0)
#
# # Import the specific values from the dataframe as a list.
# values = phos_enrich['Total'].tolist()
# values2 = values.pop(2)
#
# # Set core pie.
# trace = go.Pie(labels=labels, values=values)
#
# # Define trace as data.
# data = [trace]
#
# # Plot the data in html format.
# plot(data, filename='basicpie.html', auto_open=True)
# # --------------------------------------------------------------------------- #
# ### Pie chart for AA_mod_res_freq.
#
# # Example data
# # labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
# # values = [4500,2500,1053,500]
#
#
#
# # Import the row heading data as object.
# label0 = pd.Series(AA_mod_res_freq.index)
# # Place them into a series (not as objects).
# labels = list(label0)
#
# # Import the specific values from the dataframe as a list.
# values = AA_mod_res_freq['Total number with phospho'].tolist()
#
# # Set core pie.
# trace = go.Pie(labels=labels, values=values)
#
# # Define trace as data.
# data = [trace]
#
# # Plot the data in html format.
# plot(data, filename='basicpie2.html', auto_open=True)
#
# # --------------------------------------------------------------------------- #

### Pie chart for Multi_phos_res_freq.

# Example data
# labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
# values = [4500,2500,1053,500]

# # Import the row heading data as object.
# label0 = pd.Series(multi_phos_res_freq.index)
# # Place them into a series (not as objects).
# labels = list(label0)
#
# # Import the specific values from the dataframe as a list.
# values = multi_phos_res_freq['Frequency'].tolist()
#
#trace = go.Pie(labels=labels, values=values,
#                hoverinfo='label+percent', textinfo='value',
#                textfont=dict(size=20),
#                marker=dict(line=dict(color='#000000', width=2))
#                )
#
# # Define trace as data.
# data = [trace]
#
# # Plot the data in html format.
# plot(data, filename='basicpie3.html', auto_open=True)

# --------------------------------------------------------------------------- #

### Function to style table of significant phospho sites and render to html.
def style_df(phospho_df, kin_activities):
    """ Apply pandas "df.style" methods to subset of phospho hits dataframe 
    and render/export as html. """
    # Parse subset of significant phospho hits.
    phospho_df = phospho_df[[phospho_df.columns[0],   # Substrate.
                             phospho_df.columns[1],   # Phospho_site_ID.
                             phospho_df.columns[22],  # Substrate links.
                             phospho_df.columns[23],  # Phos-site links.
                             phospho_df.columns[24],  # Kinase links.
                             phospho_df.columns[4],   # Fold_cont_over_max.
                             phospho_df.columns[5],   # Fold_cond_over_max.
                             phospho_df.columns[9],   # Log2 fold change.
                             phospho_df.columns[13]]] # Corrected p-value.
    
    # Insert new column at index 0 to specify row position as integer. 
    idx = 0 # Set index for inserting column.
    idx_col = range(1, (len(phospho_df)+1)) # Specify range as 1:len(df)+1
    phospho_df.insert(loc=idx, column="Number", value=idx_col) # Insert.
    
    # Set CSS properties for pandas.style object.
    # CSS properties for table header/index in dataframe.
    th_props = [
      ('font-size', '16px'),
      ('font-family', 'Calibri'),
      ('text-align', 'center'),
      ('font-weight', 'bold'),
      ('color', '#000000'),
      ('background-color', '#708090'),
      ('border', '1px solid black'),
      ('height', '50px'),
      ('position', 'sticky'),
      ('position', '-webkit-sticky'),
      ('top', '50px'),
      ('z-index', '999'),
      ('padding', '5px'),
      ('background-clip', 'padding-box') # Required for firefox rendering of 
                                         # of borders on table headers. Header
                                         # background obscures bordering, hence
                                         # application of clipping.
      ]
    
    # CSS properties for table data in dataframe.
    td_props = [
      ('font-size', '12px'),
      ('border', '1px solid black'),
      ('text-align', 'center'),
      ('font-weight', 'bold'),
      ('background-clip', 'border-box') # Required for chrome to counter border
                                        # clipping applied to table headers.
      ]
    
    # Set table styles.
    styles = [
      dict(selector="th", props=th_props),
      dict(selector="td", props=td_props)
      ]
    
    # ----------------------------------------------------------------------- # 
    
    ### Sub-functions to ascertain unique phospho-hits, 
    ### and differentially colour and coerce log2 fold change columns.

    def colour_cond_uniques(phospho_df):
        """ Function to block fill with green, Log2 fold column cells that
        correspond to unique hits in control. """
        # Define colour for filling cells.
        col1 = "background-color: #5fba7d"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria. 
        mask = phospho_df["Fold control intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by boolean array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
    
    def colour_cont_uniques(phospho_df):
        """ Function to block fill with red, Log2 fold column cells that
        correspond to unique hits in condition. """
        # Define colour for filling cells.
        col1 = "background-color: #d65f5f"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria.
        mask = phospho_df["Fold condition intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by boolean array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
    
    def hide_zero_condition(phospho_df):
        """ Function to hide zero value in log2 fold column for
        condition only hits. """
        # Define colour of printed values.
        col1 = "color: #d65f5f"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria.
        mask = phospho_df["Fold condition intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by boolean array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
    
    def hide_zero_control(phospho_df):
        """ Function to hide zero value in log2 fold column for
        control only hits. """
        # Define colour of printed values.
        col1 = "color: #5fba7d"
        col2 = ""
        # Define boolean mask array. Pre-requisite for indexing a data frame,
        # that matches boolean criteria.
        mask = phospho_df["Fold control intensity over maximum"]==0 
        # Data frame matching index & and columns of "phospho_df", filled
        # with empty strings.
        df =  pd.DataFrame(col2, index=phospho_df.index, 
                           columns=phospho_df.columns)
        # Index df by booelan array and apply color to log2 fold cells,
        # with matching criteria.
        df.loc[mask, "Log2 fold change - condition over control"] = col1
        return df
        
    # ----------------------------------------------------------------------- # 
    # Pass data frame fields to multiple style methods.
    styled_phospho_df = (phospho_df.style
      # Use "background_gradient" method to apply heatmap to table
      # fold control & condition intensity over max values.                    
      .background_gradient(subset=["Fold control intensity over maximum", 
                                   "Fold condition intensity over maximum"], 
                           cmap="YlGnBu",   # Choose colour-map.
                           low=0, high=0.5) # Set color range .
                                            # Set "high" arg to low value. 
                                            # Accentuates differences between
                                            # low and high intensity values.
      
      # Use "bar" method to apply bar-chart styling to log2 fold change field.
      .bar(subset=["Log2 fold change - condition over control"], 
           align='mid',                  # Align bars with cells
           color=['#d65f5f', '#5fba7d']) # Bar color as 2 value/string tuple.
      
      # Set float precision for data - 2 significant figures. 
      .set_precision(2)
      
       # Pass CSS styling to styled table.
      .set_table_styles(styles)
      
      # Colour cells with 0 in control log2 fold column as green,
      # or red if cells with 0 in condition log2 fold column.
      .apply(colour_cond_uniques, axis=None)
      .apply(colour_cont_uniques, axis=None)
      .apply(hide_zero_condition, axis=None)
      .apply(hide_zero_control, axis=None))
    
    # ----------------------------------------------------------------------- #
    
    # Pass data frame fields to bar() style method.
    styled_kin_activities_df = (kin_activities.style               
      # Use "bar" method to apply bar-chart styling to kinase activity field.
      .bar(subset=["Kinase activity: mean of absolute fold changes"], 
           align='mid',                  # Align bars with cells
           color=['#d65f5f', '#5fba7d']) # Bar color as 2 value/string tuple.
      
      # Set float precision for data - 2 significant figures. 
      .set_precision(2)
      
       # Pass CSS styling to styled table.
      .set_table_styles(styles))
    
    # ----------------------------------------------------------------------- #
    
    # Render kinase activity table as html and export to wkdir.
    kin_act = styled_kin_activities_df.hide_index().render()
    #with open("style_kin_activities.html","w") as fp:
        #fp.write(html)

    #return html
    # Render user data phospho hits table as html and export to wkdir.
    table = styled_phospho_df.hide_index().render()
    #with open("style_ud_data.html","w") as fp:
        #fp.write(html)
        
    return  table, kin_act

# --------------------------------------------------------------------------- #

### Function to generate volcano plot from user data.
def user_data_volcano_plot(phos_table):
    """ Function to create volcano plot of signifcantly differentially 
    expressed phosho-sites from user uploaded data """
    # Parse subset of phospho-sites table.
    vp_df_subset = phos_table[[phos_table.columns[0],   # Substrate.
                               phos_table.columns[1],   # site.
                               phos_table.columns[2],   # control mean.
                               phos_table.columns[3],   # condition mean.
                               phos_table.columns[9],   # Log2 fold change.
                               phos_table.columns[14]]] # -log10(p-value).
    
    # Concatenate "substrate" and "site" fields as single string.
    vp_df_subset["Sub_site_ID"] = vp_df_subset.iloc[:, 0].astype(str)+"_"+\
                                                    vp_df_subset.iloc[:, 1] 
                                              
    # Parse substrate_sitID, log2 fold change and p-value only.                          
    vp_df_subset = vp_df_subset[[ vp_df_subset.columns[6],  # subs_site id.
                                  vp_df_subset.columns[2],  # control mean .
                                  vp_df_subset.columns[3],  # condition mean.
                                  vp_df_subset.columns[4],  # log2 fold change.
                                  vp_df_subset.columns[5]]] # -log10(p-value)
    
    # Parse hits with intensity in both conditions.
    # Necessary as fold changes for single condition hits are "inf or -inf".
    # x-axis range, for log2 fold changes in volcano plot, 
    # cannot be set properly with these entries at a lter stage.
    vp_df_subset = vp_df_subset[(vp_df_subset.iloc[:, 1] > 0) &\
                                (vp_df_subset.iloc[:, 2] > 0)]
    
    # Set core plot.
    trace = go.Scatter(
            x=vp_df_subset.iloc[:, 3],    # log2 fold change.
            y=vp_df_subset.iloc[:, 4],    # -log10(p-value).
            text=vp_df_subset.iloc[:, 0], # Set subs_id for hovering on points.
            opacity=0.9,                  # Point transparency: range = 0-1.
            mode='markers',               # Set drawing method for plot.
            marker=dict(                  # Set marker styling.
                size = 10,
                color=vp_df_subset.iloc[:, 3], # Colour set to -log10(p-value)
                colorscale='Portland',
                colorbar=dict(title='log2 fold change'),
                showscale=True),             
    )
            
    # Define trace as data.        
    data = [trace]
    
    # Pass styling to wider plot.
    layout = {
            'title': 'Volcano plot - significance of differential expression',
            'font': {
                    'family': 'Droid Serif',
                    'size': 18,
                    'color': '#3e4444'
                    },
            'height': 900,
            'width': 1100,
            'hovermode': 'closest',
            'xaxis': {
                        'title': 'Log2 fold change: condition over control',
                        'ticklen': 5,
                        'gridwidth': 2,
                        'nticks': 15,
                        'showline': True,
                        'zeroline': False
                    },
            'yaxis': {
                        'title': '-log10(corrected p-value)',
                        'ticklen': 5,
                        'gridwidth': 2
                    },
            'shapes': [
                    # Horizontal dashed line to denote permissible error rate.
                    # Error rate of 0.05 = ~1.3 (-log10 scale).
                     {
                        'type': 'line',
                        'x0': min(vp_df_subset.iloc[:, 3]),
                        'y0': 1.3,
                        'x1': max(vp_df_subset.iloc[:, 3]),
                        'y1': 1.3,
                        'line':{
                            'color': 'Black',
                            'width': 1.5,
                            'dash': 'dot'
                        },
                     },    
                    # Vertical dashed line to denote log2 fold change = -1.
                     {
                        'type': 'line',
                        'x0': -1,
                        'y0': min(vp_df_subset.iloc[:, 4]),
                        'x1': -1,
                        'y1': max(vp_df_subset.iloc[:, 4]),
                        'line':{
                            'color': 'Black',
                            'width': 1.5,
                            'dash': 'dot'
                        },
                     },    
                    # Vertical dashed line to denote log2 fold change = +1.
                     {
                        'type': 'line',
                        'x0': 1,
                        'y0': min(vp_df_subset.iloc[:, 4]),
                        'x1': 1,
                        'y1': max(vp_df_subset.iloc[:, 4]),
                        'line':{
                            'color': 'Black',
                            'width': 1.5,
                            'dash': 'dot'
                        },                                        
                },
            ]        
    }
    
    # Define figure paramters.
    fig = {
          'data': data,
          'layout': layout,
    }
    
    # Define plot as html variable for calling at Flask level.
    plotfilename = create_userfilename('volcano_plot','html')
    outfile = os.path.join(tempdir, plotfilename)
    plot(fig, filename=outfile, auto_open=False)
    #open file and read lines into variable
    with open(outfile,'r') as f:
        html = f.read()
    return html

# --------------------------------------------------------------------------- #
        
### Function to create wordcluds and frequency charts.    
def wordcloud_freq_charts(kin_word_str,
                          subs_sites_word_str,
                          kinase_freq,
                          kinase_target_freq):
    """
    Pass word strings and frequencies to create wordclouds and
    plot frequency charts for kinase and substrate_sites in
    the global phospho only data. "
    :param kin_word_str: string of multiple kinases
    :param subs_sites_word_str: string of multiple subs_sites
    :param kinase_freq: int
    :param kinase_target_freq: int
    :return: string variables of filenames
    """

    # Create wordcloud for kinases.
    kin_wcloud= create_userfilename('kin_wordcloud','png')
    outfile = os.path.join(tempdir,kin_wcloud)
    # Pass string variables to wordcloud function.
    WordCloud(collocations=False, background_color="gray", max_words=30,
                 relative_scaling=0.5, colormap="RdBu").generate(kin_word_str).\
                           to_file(outfile)

    # Create wordcloud for substrate_sites.
    subs_sites_wcloud = create_userfilename('subs_sites_wordcloud', 'png')
    outfile = os.path.join(tempdir, subs_sites_wcloud)

    WordCloud(collocations=False, background_color="gray", max_words=30,
                 relative_scaling=0.5, colormap="RdBu").\
                 generate(subs_sites_word_str).to_file(outfile)
                                 
    # ----------------------------------------------------------------------- #
    # Plot kinase frequency - top30.
    plt.figure(figsize=(10,7))
    kinase_freq.sort_values(ascending=False).\
                plot.bar(width=0.85, alpha=0.75)
    plt.xticks(rotation=75)
    plt.xlabel("Kinase", fontsize="large", 
               fontstyle="italic", fontweight="bold")
    plt.ylabel("Frequency", fontsize="large", 
               fontstyle="italic", fontweight="bold")
    kin_freq = create_userfilename('Kinase_freq_top_30_Bar', 'png')
    outfile = os.path.join(tempdir, kin_freq)

    plt.savefig(outfile, bbox_inches="tight", dpi=300)
    
    # Plot subs_sites frequency - top30.
    plt.figure(figsize=(10,7))
    kinase_target_freq.sort_values(ascending=False).\
                       plot.bar(width=0.85, alpha=0.75)
    plt.xticks(rotation=75)
    plt.xlabel("Substrate & site", fontsize="large", 
               fontstyle="italic", fontweight="bold")
    plt.ylabel("Frequency", fontsize="large", 
               fontstyle="italic", fontweight="bold")
    kin_target_freq = create_userfilename('Kin_target_freq_top_30_Bar', 'png')
    outfile = os.path.join(tempdir, kin_target_freq)

    plt.savefig(outfile, bbox_inches="tight", dpi=300)

    #return filenames of plot pngs
    return kin_wcloud, subs_sites_wcloud, kin_freq, kin_target_freq
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # set up runs for testing functions
    file = os.path.join('user_data', 'az20.tsv')

    data_or_error = user_data_check(file)

    styno, sty = create_filtered_dfs(data_or_error)

    corrected_p = correct_pvalue(sty)

    full_sty_sort, parsed_sty_sort, db_kin_dict = table_sort_parse(corrected_p)

    phos_enrich, AA_mod_res_freq, multi_phos_res_freq, prot_freq = \
        data_extract(full_sty_sort, styno)

    kinase_target_freq, kinase_freq, kin_word_str, subs_sites_word_str, \
    kinase_activities = kinase_analysis(db_kin_dict, parsed_sty_sort)

    style_df(parsed_sty_sort, kinase_activities)

    ud_volcano = user_data_volcano_plot(full_sty_sort)

    stuff = wordcloud_freq_charts(kin_word_str,
                                         subs_sites_word_str,
                                         kinase_freq,
                                         kinase_target_freq)

    pie_ch = pie_chart(AA_mod_res_freq, "Total", "testpie")