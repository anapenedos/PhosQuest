# standard imports
from sqlalchemy import and_, or_
from sqlalchemy.orm import Load

# project imports
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Phosphosite, kinases_phosphosites_table
from PhosphoQuest_app.data_access.class_functions import get_classes_key_attrs


def records_from_join_res(list_of_tuples):
    """
    Given a list of tuples from the result of a sqlalchemy join query returns
    a dictionary mapping a class to a set of instances of that class.

    :param list_of_tuples: sqlalchemy join query result (list of tuples)
    :return: dictionary of classes to unique instances set (dict)
             {Class: {inst1, inst2}}
    """
    class_instances = {}  # {Class: {inst1, inst2}}
    # iterate through each substrate/phosphosite/kinase
    for instances_tuple in list_of_tuples:
        # iterate through each instance inthe tuple
        for instance in instances_tuple:
            if instance:
                # add a dict key for each type of class
                class_obj = type(instance)
                cls_set = class_instances.setdefault(class_obj, set())
                cls_set.add(instance)
    return class_instances


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

    :param txt_tuple_iter: an iterable of tuples where the 0 element of the
                           tuple is the gene/name and element 1 is the
                           accession/ID number of the instance.
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

    :param txt_tuple_iter: an iterable of tuples where the 0 element of the
                          tuple is the text to display in the link and element
                          1 is the key value to build the link (iter of tuples)
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
             data frame with individual kinases >
    """
    # open sqlite session
    session = create_sqlsession()

    # create dictionary to link user phosphosites to db entries
    # 'Substrate Entry in DB': [{'ACC1'}, 'not in DB', ...] accessions are str
    # 'Phosphosite Entry in DB': [{id1}, 'not in DB', ...] ids are integers
    # 'Associated Kinases': [{'ACCa', 'ACCb'}, 'not in DB', ...]
    db_links = {Substrate: [],
                Phosphosite: [],
                Kinase: []}

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
    query = session.query(Substrate, Phosphosite, Kinase)\
        .outerjoin(Phosphosite)\
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
        # or_ None allows modified residue not to be present in DB if substrate
        # is
        # query_res format is [(substrate instance, phosphosite instance /
        # None, kinase instance 1 / None), (subs, phos, kin2)]
        # the kinase instance is the only one that changes in
        # each substrate/phosphosite/kinase tuple in query_res
        query_res = query.filter(and_(
            Substrate.subs_gene == s_gene,
            or_(Phosphosite.phos_modified_residue == residue,
                Phosphosite.phos_modified_residue == None))).all()
        # if the substrate is not in the DB, 'not in DB' is added to the three
        # columns in db_links dict
        if len(query_res) == 0:
            for key in db_links:
                db_links[key].append(not_in_db)
        else:
            # dict of classes to unique instances set from the query results
            # {Class: {inst1, inst2}}
            class_records = records_from_join_res(query_res)

            # add relevant instance information to dictionaries
            record_info = {}
            # substrates (always present)
            record_info[Substrate] = extract_record_info(
                class_records[Substrate], ('subs_gene', 'subs_accession'))
            # if phosphosites were found add info to substrate-centric dict
            if Phosphosite in class_records:
                record_info[Phosphosite] = extract_record_info(
                    class_records[Phosphosite], ('phos_modified_residue',
                                                 'phos_group_id'))
            # if kinases were found add the kinase gene(s) to both
            # substrate-centric and kinase-centric dictionaries
            if Kinase in class_records:
                record_info[Kinase] = extract_record_info(
                    class_records[Kinase], ('kin_gene', 'kin_accession'))
                for kin in record_info[Kinase]:
                    kinase_gene = kin[0]
                    new_set = kin_to_ud.setdefault(kinase_gene, set())
                    new_set.add((s_gene, residue))

            # append the new values to the columns dict db_links
            for class_obj in db_links:
                if class_obj in record_info:
                    to_append = record_info[class_obj]
                else:
                    to_append = not_in_db
                db_links[class_obj].append(to_append)
        # remove all objects found in loop from session to reduce memory usage
        session.expire_all()
    session.close()

    # change key/column names
    db_links['Substrate/Isoform in DB (gene name)'] = \
        db_links.pop(Substrate)
    db_links['Phosphosite in DB (ID)'] = \
        db_links.pop(Phosphosite)
    db_links['Kinase in DB\n(gene name)'] = \
        db_links.pop(Kinase)

    return db_links, kin_to_ud


if __name__ == "__main__":
    # standard imports
    import os

    from PhosphoQuest_app.service_scripts.user_data_crunch \
        import user_data_check
    from PhosphoQuest_app.service_scripts.userdata_display import run_all
    from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
    from sqlalchemy.orm import Load
    import pandas as pd

    ad = run_all(user_data_check(os.path.join('user_data',
                                              'az20.tsv')))

    sty = ad['full_sty_sort']
    styno = ad['parsed_sty_sort']

    # sites_dict, kin_dict = link_ud_to_db(styno)

    # session = create_sqlsession(session_type='pandas_sql')
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