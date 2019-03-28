# standard imports
from sqlalchemy import and_, or_
from sqlalchemy.orm import Load

# project imports
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Phosphosite, kinases_phosphosites_table
from PhosphoQuest_app.data_access.class_functions import get_classes_key_attrs


def distinct_records(query_res):
    """
    Given a list of tuples from the result of a sqlalchemy join query returns
    unique record info for the substrates, phosphosites and kinases in the query
    result.

    :param query_res: sqlalchemy join query result (list of tuples)
    :return: three sets of unique substrate, phosphosite and kinase records'
             info (unique_subs, unique_phos, unique_kin sets)
    """
    # collect distinct substrate , phosphosite and kinase record info
    # from all records retrieved in the query
    unique_subs = set()
    unique_phos = set()
    unique_kin = set()
    for record in query_res:
        subs_info = (record[0], record[1])  # (subs_gene, subs_acc)
        unique_subs.add(subs_info)
        # The record info tuples retrieved when the phosphosite is not
        # found in the DB is len 2, while those resulting from the
        # 3-table join are len 6
        if len(record) > 2:
            if record[2]:  # only add if not None
                # collect distinct phosphosite records from record info
                # retrieved in join query
                phos_info = (record[2], record[3])  # (phos_rsd, phos_id)
                unique_phos.add(phos_info)
            if record[4]:  # only add if not None
                # collect distinct kinase record info from records
                # retrieved in join query
                kin_info = (record[4], record[5])  # (kin_gene, kin_acc)
                unique_kin.add(kin_info)

    return unique_subs, unique_phos, unique_kin


def extract_record_info(instances, info_needed_tuple):
    """
    From a list of sqlalchemy class objects (records from a single table), get
    the instance attributes specified in the info needed tuple.

    :param instances: an iterable containing class instances (inst iter)
    :param info_needed_tuple: tuple containing the attributes required
                              (tuple of strs)
    :return: list of info tuples in the same order as info_needed_tuple sorted
             by first element of tuple (list of tuples)
             [(info1, info2), ...]
    """
    records_info = []
    for instance in instances:
        info = tuple(getattr(instance, attr)
                     for attr in info_needed_tuple)
        records_info.append(info)
    return sorted(records_info)


def create_db_strs(txt_tuple_iter):
    """
    From an iterable containing DB info for records in DB or 'not in DB' when no
    records were found, return info formatted as string.

    :param txt_tuple_iter: an iterable of strings and tuples where the 0 element
                           of the tuple is the gene/name and element 1 is the
                           accession/ID number of the instance
                           (iter of tuples and strs)
    :return: string containing info to each entry (str)
    """
    # a line can be [('Q8WYB5',)] or 'not in DB' or
    # [('Q8WYB6',), ('Q8WYB7',)]
    if txt_tuple_iter != 'not in DB':
        info_joiner = '/'.join
        # a record can be ('Q8WYB5',) or ('GENE1', 'Q8WYB7') or (12,)
        rec_strs = [info_joiner(map(str, record)) for record in txt_tuple_iter]
        new_line = ', '.join(rec_strs)
    else:
        new_line = txt_tuple_iter
    return new_line


def format_db_strs(db_links, headers=False):
    """
    Formats a db_links dictionary to show in web app.

    :param db_links: dictionary listing processed query results matching each
                     line of a user data frame (dict)
                     col: [[('Q8WYB5',)],
                           'not in DB',
                           [('Q8WYB6',), ('Q8WYB7',)]]
    :headers: convert dict keys (column headers) to string when column headers
              are class objects (boolean)
    :return: dictionary with more readable lines (dict)
             col: ['Q8WYB5', 'not in DB', 'Q8WYB6 Q8WYB7']
    """
    # [('Q8WYB5',)], 'not in DB', [('Q8WYB6',), ('Q8WYB7',)]
    tidy_db_links = {}
    for col in db_links:
        # a column is of format
        # [[('Q8WYB5',)], 'not in DB', [('Q8WYB6',), ('Q8WYB7',)]]
        # format lines of each column to show as str
        tidy_db_links[col] = []
        for line in db_links[col]:
            # a line can be [('Q8WYB5',)] or 'not in DB' or
            # [('Q8WYB6',), ('Q8WYB7',)]
            if type(line) != str:
                info_joiner = '/'.join
                # a record can be ('Q8WYB5',) or ('GENE1', 'Q8WYB7') or (12,)
                rec_strs = [info_joiner(map(str, record)) for record in line]
                new_line = ', '.join(rec_strs)
            else:
                new_line = line
            tidy_db_links[col].append(new_line)

        if headers:
            # rename db_links keys to present as str
            new_name = col.__name__ + ' DB links'
            tidy_db_links[new_name] = tidy_db_links.pop(col)
    return tidy_db_links


def create_db_links(txt_tuple_iter, detail_page):
    """
    From an iterable containing DB info for records in DB or 'not in DB' when no
    instances were found, returns info formatted as url links to detail pages of
    the records.

    :param txt_tuple_iter: an iterable of strings and tuples where the 0 element
                          of the tuple is the text to display in the link and
                          element 1 is the key value to build the link
                          (iter of tuples and strs)
    :detail_page: the details page relevant to the entries being processed (str)
    :return: string containing links to each entry (str)
    """
    if txt_tuple_iter != 'not in DB':
        line_links = []
        for txt, key in txt_tuple_iter:
            line_links.append('<a target="_blank" href="/%s/%s">%s</a>'
                               % (detail_page, key, txt))
        line = ', '.join(line_links)
    else:
        line = 'not in DB'
    return line


def format_db_links(db_links):
    """
    Formats a db_links dictionary to show in web app as links to detail pages.

    :param db_links: dictionary listing processed query results matching each
                     line of a user data frame (dict)
                     col: [[('Q8WYB5',)],
                           'not in DB',
                           [('Q8WYB6',), ('Q8WYB7',)]]
    :return: dictionary with more readable lines (dict)
             col: ['Q8WYB5', 'not in DB', 'Q8WYB6 Q8WYB7']
    """
    # [('Q8WYB5',)], 'not in DB', [('Q8WYB6',), ('Q8WYB7',)]
    tidy_db_links = {}

    # detail page route for each column
    detail_pages = {Kinase: 'kin_detail',
                    Substrate: 'sub_detail',
                    Phosphosite: 'phosites_detail'}

    for col in db_links:
        # a column is of format
        # [[('Q8WYB5',)], 'not in DB', [('Q8WYB6',), ('Q8WYB7',)]]
        # format lines of each column to show as str
        tidy_db_links[col] = [create_db_links(line, detail_pages[col])
                              for line in db_links[col]]

    return tidy_db_links


def link_ud_to_db(user_data_frame):
    """
    Check substrates and phosphosites in the user data against the database and
    return DB info of substrates, phosphosites and kinases records matching user
    data.

    :param user_data_frame: a data frame containing the significant hits in the
                            user csv file (pandas df)
    :return: data frame column containing user sites > db entry / kinases
             data frame with individual kinases > gene / site
    """
    # open sqlite session
    session = create_sqlsession()

    # create dictionary to link user phosphosites to db entries
    # 'Substrate Entry in DB': [{('gene1', 'ACC1'),...}, 'not in DB', ...]
    # 'Phosphosite Entry in DB': [{('rsd1', id1),...}, 'not in DB', ...] ids are integers
    # 'Associated Kinases': [{('gene1', 'ACC1'),...}, 'not in DB', ...]
    db_links = {'Substrate/Isoform in DB (gene name)': [],
                'Phosphosite in DB (ID)': [],
                'Kinase in DB\n(gene name)': []}

    # create dictionary for kinase-centric analysis data frame
    # 'KIN_ACC': {('SUB_GENE', 'RSD'),...}
    kin_to_ud = {}

    # not found in DB message
    not_in_db = 'not in DB'

    # 3 table query left outer joining on substrate
    # one substrate can have multiple phosphosites; outer join allows for
    # return of a substrate if user modified residue has not been included in
    # DB
    # Kinases are associated with phosphosites, there may be no kinases for a
    # site
    query = session.query(Substrate.subs_gene, Substrate.subs_accession,
                          Phosphosite.phos_modified_residue,
                          Phosphosite.phos_group_id,
                          Kinase.kin_gene, Kinase.kin_accession)\
        .outerjoin(Phosphosite)\
        .outerjoin(kinases_phosphosites_table)\
        .outerjoin(Kinase)

    # iterate through each line of the user data frame
    for index, row in user_data_frame.iterrows():
        # substrate gene in the line
        # some substrates may have 'GENE_species', hence split on '_'
        s_gene = row['Substrate (gene name)'].split('_')[0]
        # modified residue in the line
        residue = row['Phospho site ID']
        # filter the query based on substrate gene and modified residue
        # or_ None allows modified residue not to be present in DB if substrate
        # is
        # query_res format is [(substrate instance, phosphosite instance /
        # None, kinase instance 1 / None), (subs, phos, kin2)]
        # the kinase instance is the only one that changes in
        # each substrate/phosphosite/kinase tuple in query_res
        query_res = query.filter(and_(
            Substrate.subs_gene == s_gene,
            Phosphosite.phos_modified_residue == residue)).all()

        # query_res can be [], [one], [several, records]
        # where each record is a tuple
        # (gene, accession, residue, grp id, kin gene, kin acc)

        # if query_res is [] because the phosphosite is not in DB, we still want
        # the substrate info available in the DB
        if len(query_res) == 0:
            subs_only = session.query(
                Substrate.subs_gene, Substrate.subs_accession)\
                .filter(Substrate.subs_gene == s_gene).all()
            query_res = subs_only

        # if the substrate is not in the DB 'not in DB' is added to the
        # three entries/columns in db_links dict
        if len(query_res) == 0:
            for col in db_links:
                db_links[col].append(not_in_db)

        else:
            unique_subs, unique_phos, unique_kin = distinct_records(query_res)

            # if kinases were found in the query, map kinase genes to the user
            # gene and residue
            for kin in unique_kin:
                kinase_gene = kin[0]
                new_set = kin_to_ud.setdefault(kinase_gene, set())
                new_set.add((s_gene, residue))

            # append the new values to the columns dict db_links
            # if there are no records in any of the sets containing unique
            # records replace the empty set with 'not in DB'
            db_links['Substrate/Isoform in DB (gene name)'].append(
                unique_subs if len(unique_subs) != 0 else not_in_db)
            db_links['Phosphosite in DB (ID)'].append(
                unique_phos if len(unique_phos) != 0 else not_in_db)
            db_links['Kinase in DB\n(gene name)'].append(
                unique_kin if len(unique_kin) != 0 else not_in_db)

        # remove all objects found in loop from session to reduce memory usage
        session.expire_all()
    session.close()

    return db_links, kin_to_ud


"""
1. ud df
2. from gene col, get subs in db
"""
if __name__ == "__main__":
    # standard imports
    import os

    from PhosphoQuest_app.service_scripts.user_data_crunch \
        import user_data_check
    from PhosphoQuest_app.service_scripts.userdata_display import run_all
    from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
    from sqlalchemy.orm import Load
    import pandas as pd

    # ad = run_all(user_data_check(os.path.join('user_data',
    #                                           'az20.tsv')))
    #
    # sty = ad['full_sty_sort']
    # styno = ad['parsed_sty_sort']
    # styno.to_csv('styno.csv')
    styno = pd.read_csv('styno.csv')

    def subs_in_db(gene_name):
        session = create_sqlsession()
        query_res = session.query(Substrate.subs_gene, Substrate.subs_accession)\
                           .filter_by(subs_gene=gene_name).all()
        session.close()
        if len(query_res) == 0:
            result = 'not in DB'
        else:
            result = query_res
        return result

    def phos_in_db(subs_list, residue):

        session = create_sqlsession()

        phos_set = set()
        kin_set = set()
        if subs_list != 'not in DB':
            for substrate in subs_list:
                subs_acc = substrate[1]  # accession is in position 1 of tuple
                query_res = session.query(Phosphosite.phos_modified_residue,
                                          Phosphosite.phos_group_id,
                                          Phosphosite.phos_in_substrate,
                                          Phosphosite.phosphorylated_by)\
                                   .filter(and_(Phosphosite. phos_in_substrate == subs_acc,
                                                Phosphosite.phos_modified_residue == residue)).all()
                for record in query_res:
                    phos_set.add((record[0], record[1]))  # (residue, grp_id)
                    record_kinases = record[4]
                    for kinase in record_kinases:
                        kin_set.add(kinase)
            session.close()
            result = (phos_set, kin_set)
        else:
            result = 'not in DB'
        return result


    fields = [Substrate.subs_gene, Substrate.subs_accession]
    session = create_sqlsession()
    query = session.query(*fields)\
        .filter_by(subs_gene='NEDD4').all()
    print(query)
    print(subs_in_db('NEDD4'))
    # p_res = session.query(Phosphosite.phos_modified_residue,
    #                           Phosphosite.phos_group_id,
    #                           Phosphosite.phos_in_substrate,
    #                           Phosphosite.phosphorylated_by) \
    #     .filter(and_(Phosphosite.phos_in_substrate == 'P46934-4',
    #                  Phosphosite.phos_modified_residue == 'S743')).all()
    # for phos in p_res:
    #     print(phos)
    q1 = session.query(Substrate.subs_gene, Substrate.subs_accession,
                          Phosphosite.phos_modified_residue,
                          Phosphosite.phos_group_id,
                          Kinase.kin_gene, Kinase.kin_accession) \
        .outerjoin(Phosphosite) \
        .outerjoin(kinases_phosphosites_table) \
        .outerjoin(Kinase).filter(Substrate.subs_gene == 'NEDD4')
    q1r = q1.all()
    q2 = q1.filter(Phosphosite.phos_modified_residue == 'S743')
    q2r = q2.all()
    session.close()
    print(q1r)
    print(q2r)
    print(len(q1r))
    # print(phos_in_db([('NEDD4', 'P46934'), ('NEDD4', 'P46934-3'), ('NEDD4', 'P46934-4')], 'S743'))
    # query = session.query(Substrate, Phosphosite, Kinase)\
    #         .outerjoin(Phosphosite)\
    #         .outerjoin(kinases_phosphosites_table)\
    #         .outerjoin(Kinase)\
    #         .options(Load(Substrate).load_only("subs_gene"),
    #                  Load(Phosphosite).load_only("phos_modified_residue"),
    #                  Load(Kinase).load_only("kin_gene"))
    # subs_phos_kin_subset_df = pd.read_sql(subs_phos_kin_query.\
    #                                      statement,\
    #                                      subs_phos_kin_query.session.bind)