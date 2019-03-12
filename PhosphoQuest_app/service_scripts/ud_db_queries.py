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
    class_instances = {}
    for instances_tuple in list_of_tuples:
        for instance in instances_tuple:
            if instance:
                class_obj = type(instance)
                cls_set = class_instances.setdefault(class_obj, set())
                cls_set.add(instance)
    return class_instances


def extract_record_info(instances, info_needed_tuple):
    """
    From a list of sqlalchemy class objects (table records), get the instance
    attributes specified in the info needed tuple.

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


def format_db_links(db_links, headers=False):
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
                rec_strs = []
                # a record can be ('Q8WYB5',) or ('GENE1', 'Q8WYB7') or (12,)
                for record in line:
                    rec_strs.append('/'.join(map(str, record)))
                new_line = ', '.join(rec_strs)
            else:
                new_line = line
            tidy_db_links[col].append(new_line)

        if headers:
            # rename db_links keys to present as str
            new_name = col.__name__ + ' DB links'
            tidy_db_links[new_name] = tidy_db_links.pop(col)
    return tidy_db_links


def link_ud_to_db(user_data_frame):
    """
    Check substrates and phosphosites in the user data against the data base
    and return primary keys to substrates, phosphosites and kinases tables.

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

    # primary key attribute for each class
    db_key_attrs = get_classes_key_attrs(db_links, single_key=True)

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
                class_records[Substrate], ('subs_accession',))
            # if phosphosites were found add info to substrate-centric dict
            if Phosphosite in class_records:
                record_info[Phosphosite] = extract_record_info(
                    class_records[Phosphosite], ('phos_group_id',))
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

    # format db_links dict
    # show as strings
    tidy_db_links = format_db_links(db_links)
    # change key/column names
    tidy_db_links['Substrate/Isoform in DB (accession)'] = \
        tidy_db_links.pop(Substrate)
    tidy_db_links['Phosphosite in DB (ID)'] = \
        tidy_db_links.pop(Phosphosite)
    tidy_db_links['Kinase in DB\n(gene/accession)'] = \
        tidy_db_links.pop(Kinase)

    return tidy_db_links, kin_to_ud