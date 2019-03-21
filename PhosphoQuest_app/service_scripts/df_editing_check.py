from PhosphoQuest_app.service_scripts.df_editing import create_db_kin_links
#
# # testing split multi value lines function
# df=pd.DataFrame(data=[['1 3',' 2','3,4,5'], ['ajh jh', 'b', 'ch,   dhh jj ']],
#                 columns=['A','B','C'])
# print(df, '\n')
# sdf = split_multi_value_rows_in_df(df, 'C', ',')
# print(sdf)

# TODO rm or update test

def create_db_kin_links_test():
    # test sets
    t1 = 'not in DB'
    t2 = {'P49841'}
    t3 = {'O14757', 'Q05655'}

    # test set results expected
    e1 = 'not in DB'
    e2 = "<a href='/kin_detail/P49841'>P49841</a> "
    e3 = "<a href='/kin_detail/O14757'>O14757</a> " \
         "<a href='/kin_detail/Q05655'>Q05655</a> "

    # create_db_kin_links results
    r1 = create_db_kin_links(t1)
    r2 = create_db_kin_links(t2)
    r3 = create_db_kin_links(t3)

    failed = []
    for test in [(t1, e1, r1), (t2, e2, r2), (t3, e3, r3)]:
        print(test)
        if test[1] != test[2]:
            failed.append(test[0])

    return failed



# small_kin_df_lnk = ['not in DB', {'O14757', 'Q05655'}, {'P49841'}]