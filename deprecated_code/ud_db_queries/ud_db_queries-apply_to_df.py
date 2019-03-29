# standard imports
from sqlalchemy import and_, or_
from sqlalchemy.orm import Load

# project imports
from PhosQuest_app.data_access.db_sessions import create_sqlsession
from PhosQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Phosphosite, kinases_phosphosites_table
from PhosQuest_app.data_access.class_functions import get_classes_key_attrs


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


def link_ud_to_db(gene, residue):
    # TODO docstr

    # not found in DB message
    not_in_db = 'not in DB'

    # create dictionary for kinase-centric analysis data frame
    # 'KIN_ACC': {('SUB_GENE', 'RSD'),...}
    kin_to_ud = {}

    # open sqlite session
    session = create_sqlsession()

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
        .outerjoin(Kinase)\
        .options(Load(Substrate).load_only("subs_gene"),
                 Load(Phosphosite).load_only("phos_modified_residue"),
                 Load(Kinase).load_only("kin_gene"))

    # substrate gene in the line
    # some substrates may have 'GENE_species', hence split on '_'
    s_gene = gene.split('_')[0]

    # filter the query based on substrate gene and modified residue
    # query_res format is [(gene, acc, rsd, grp id,
    # kin gene / None, kin acc / None)]
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
    # three link entries/columns
    if len(query_res) == 0:
        new_line = (not_in_db, not_in_db, not_in_db)
        # print(new_line)

    else:
        unique_subs, unique_phos, unique_kin = distinct_records(query_res)
        if unique_kin:
            # if kinases were found in the query, map kinase genes to the user
            # gene and residue
            for kin in unique_kin:
                kinase_gene = kin[0]
                new_set = kin_to_ud.setdefault(kinase_gene, set())
                new_set.add((s_gene, residue))


        # append the new values to the columns dict db_links
        # if there are no records in any of the sets containing unique
        # records replace the empty set with 'not in DB'
        sub_line = sorted(unique_subs) if unique_subs else not_in_db
        phos_line = sorted(unique_phos) if unique_phos else not_in_db
        kin_line = sorted(unique_kin) if unique_kin else not_in_db
        new_line = list((sub_line, phos_line, kin_line))

    # remove all objects found in loop from session to reduce memory usage
    session.expire_all()
    session.close()
    if len(new_line) != 3:
        print(new_line)
    return new_line


if __name__ == "__main__":
    from PhosQuest_app.data_access.db_sessions import create_sqlsession
    import pandas as pd
    from datetime import datetime

    styno = pd.read_csv('styno.csv')
    for i in range(5):
        start_time = datetime.now()
        styno[['Substrate/Isoform in DB (gene name)',
              'Phosphosite in DB (ID)',
              'Kinase in DB\n(gene name)']] = styno.apply(
            lambda row: pd.Series(link_ud_to_db(row['Substrate (gene name)'],
                                      row['Phospho site ID'])),
            axis=1)
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print(elapsed_time)
    print(styno)
