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
    unique record info for the substrates, phosphosites and kinases in the
    query result.

    :param query_res: sqlalchemy join query result (list of tuples)
    :return: three sets of unique substrate, phosphosite and kinase records'
             info (unique_subs, unique_phos, unique_kin; sets)
    """
    # collect distinct substrate, phosphosite and kinase record info
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
            if record[2]:  # only add phosphosite info if not None
                # collect distinct phosphosite records from record info
                # retrieved in join query
                phos_info = (record[2], record[3])  # (phos_rsd, phos_id)
                unique_phos.add(phos_info)
            if record[4]:  # only add kinase info if not None
                # collect distinct kinase record info from records
                # retrieved in join query
                kin_info = (record[4], record[5])  # (kin_gene, kin_acc)
                unique_kin.add(kin_info)

    return unique_subs, unique_phos, unique_kin


def create_db_strs(txt_tuple_iter):
    """
    From an iterable containing DB info for records in DB or 'not in DB' if no
    records were found, return info formatted as string.

    :param txt_tuple_iter: an iterable of strings and tuples where the 0
                           element of the tuple is the gene/residue and element
                           1 is the DB key of the record
                           (iter of tuples and strs)
    :return: string containing info to each entry (str)
    """
    # a line can be [('Q8WYB5',)] or 'not in DB' or [('Q8WYB6',), ('Q8WYB7',)]
    if txt_tuple_iter != 'not in DB':
        info_joiner = '/'.join
        # a record can be ('Q8WYB5',) or ('GENE1', 'Q8WYB7') or (12,)
        # converts integers into strs, joins info in each tuple with a '/'
        rec_strs = [info_joiner(map(str, record)) for record in txt_tuple_iter]
        # joins all info with ', ' to produce new line
        new_line = ', '.join(rec_strs)
    # if there was no info in DB, returns the same: 'not in DB'
    else:
        new_line = txt_tuple_iter
    return new_line


def create_db_links(txt_tuple_iter, link_format):
    """
    From an iterable containing DB info for records in DB or 'not in DB' if no
    records were found, returns info formatted as url links to detail pages of
    the records.

    :param txt_tuple_iter: an iterable of strings and tuples where the 0
                           element of the tuple is the gene/residue and element
                           1 is the DB key of the record
                           (iter of tuples and strs)
    :link_format: a tuple where the 0th element is the detail page relevant for
                  the records passed and element 1 is a tuple of the position
                  of the txt to display in the txt_tuple_iter and the position
                  of the DB key in the txt_tuple_iter
                  ('page', (txt, position, key position)) (len 2 tuple)
    :return: string containing URL links to each entry (str)
    """
    if txt_tuple_iter != 'not in DB':
        detail_page = link_format[0]
        line_links = []
        for info in txt_tuple_iter:
            key = info[link_format[1][1]]
            txt = info[link_format[1][0]]
            line_links.append('<a target="_blank" href="/%s/%s">%s</a>'
                               % (detail_page, key, txt))
        line = ', '.join(line_links)
    else:
        line = 'not in DB'
    return line


def link_ud_to_db(user_data_frame):
    """
    Check substrates and phosphosites in the user data against the database and
    return DB info of substrates, phosphosites and kinases records matching the
    user data.

    :param user_data_frame: a data frame containing the significant hits in the
                            user csv file (pandas df)
    :return db_links: dictionary that will be converted into df columns linking
                      to DB of the same length as user_data_frame. Dict keys
                      are column headings and dict values are lists that will
                      become the column values, each element in the list
                      becoming a line (dict)
    :return kin_to_ud: dictionary that will be used for the kinase-centric
                       analyses, where keys are unique kinases associated with
                       user sites and values are the user substrates/sites
                       associated with the kinase (dict)
    """
    # open sqlite session
    session = create_sqlsession()

    # create dictionary to link user phosphosites to db entries
    # substrates col: [{('gene1', 'ACC1'),...}, 'not in DB', ...]
    # sites col: [{('rsd1', id1),...}, 'not in DB', ...] ids are integers
    # kinases col: [{('gene1', 'ACC1'),...}, 'not in DB', ...]
    db_links = {'Substrate/Isoform in DB (accession)': [],
                'Phosphosite in DB (DB ID)': [],
                'Kinase in DB\n(gene)': []}

    # create dictionary for kinase-centric analysis data frame
    # 'kin_gene': {('subs_gene', 'residue'),...}
    kin_to_ud = {}

    # not found in DB message
    not_in_db = 'not in DB'

    # 3 table query left joining on substrate
    # given that we need to filter on phosphosite residue and to reduce number
    # of entries returned, inner join on phosphosite is used
    # Kinases are associated with phosphosites, there may be no kinases for a
    # site;
    # one substrate/phosphosite can be associated with multiple kinases: outer
    # join allows for return of a substrate/site if no kinases are found in DB
    query = session.query(
        Substrate.subs_gene, Substrate.subs_accession,
        Phosphosite.phos_modified_residue, Phosphosite.phos_group_id,
        Kinase.kin_gene, Kinase.kin_accession)\
        .join(Phosphosite)\
        .outerjoin(kinases_phosphosites_table)\
        .outerjoin(Kinase)\
        .options(Load(Substrate).load_only("subs_gene"),
                 Load(Phosphosite).load_only("phos_modified_residue"),
                 Load(Kinase).load_only("kin_gene"))

    # iterate through each line of the user data frame
    for index, row in user_data_frame.iterrows():
        # substrate gene in the line
        # some substrates may have 'GENE_species', hence split on '_'
        s_gene = row['Substrate (gene name)'].split('_')[0]
        # modified residue in the line
        residue = row['Phospho site ID']
        # filter the query based on substrate gene and modified residue
        # query_res format is
        # [(subs_gene, subs_acc, site_rsd, site_id, kin_gene, kin_acc),...]
        # or []
        query_res = query.filter(and_(
            Substrate.subs_gene == s_gene,
            Phosphosite.phos_modified_residue == residue)).all()

        # query_res can be [], [one], [several, records]

        # if query_res is [] because the phosphosite is not in DB, we want to
        # retrieve any substrate info available in the DB
        if not query_res:
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
            # de-duplicate records found
            unique_subs, unique_phos, unique_kin = distinct_records(query_res)

            # if kinases were found in the query, map kinase genes to the user
            # gene and residue
            for kin in unique_kin:
                kinase_gene = kin[0]
                kin_set = kin_to_ud.setdefault(kinase_gene, set())
                kin_set.add((s_gene, residue))

            # append the new values to the columns dict db_links
            # if there are no records in any of the sets containing unique
            # records replace the empty set with 'not in DB'
            db_links['Substrate/Isoform in DB (accession)'].append(
                unique_subs if unique_subs else not_in_db)
            db_links['Phosphosite in DB (DB ID)'].append(
                unique_phos if unique_phos else not_in_db)
            db_links['Kinase in DB\n(gene)'].append(
                unique_kin if unique_kin else not_in_db)

        # remove all objects found in loop from session to reduce memory usage
        session.expire_all()
    session.close()

    return db_links, kin_to_ud


if __name__ == "__main__":
    from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
    import pandas as pd
    from datetime import datetime

    styno = pd.read_csv('styno.csv')
    for i in range(5):
        start_time = datetime.now()
        d1, d2 = link_ud_to_db(styno)
        db_ud_df = pd.DataFrame.from_dict(d1, orient='index').transpose()

        # Concatenate full phospho table with DB user data matches.
        # Note: input dataframe "Filtered_df" index isn't ordered 1, 2, 3...,
        # due to previous operations.
        # reset_index() extracts index to column, and uses default i.e. 1, 2, 3...,
        # as new index. Reseting the index is required, as dataframe
        # concatenation is by column indices!
        filtered_df = pd.concat([styno.reset_index(drop=True),
                                 db_ud_df.reset_index(drop=True)],
                                axis=1)
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print(elapsed_time)
