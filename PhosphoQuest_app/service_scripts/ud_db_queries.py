# standard imports
from sqlalchemy import and_, or_
from sqlalchemy.orm import Load

# project imports
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Phosphosite, kinases_phosphosites_table
from sqlalchemy.inspection import inspect


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

    # create dictionary to form columns to be displayed
    # 'Substrate Entry in DB': ['ACC1', 'not in DB', ...] accessions are stings
    # 'Phosphosite Entry in DB': [id1, 'not in DB', ...] ids are integers
    # 'Associated Kinases': [['ACCa', 'ACCb'], 'not in DB', ...]
    db_links = {Substrate: [],
                Phosphosite: [],
                Kinase: []}

    # primary key attribute for each class
    db_key_attrs = {}
    for class_name in db_links:
        key_attr = inspect(class_name).primary_key[0].name
        db_key_attrs[class_name] = key_attr

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
        gene = row['Substrate (gene name)'].split('_')[0]
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
            Substrate.subs_gene == gene,
            or_(Phosphosite.phos_modified_residue == residue,
                Phosphosite.phos_modified_residue == None))).all()
        # if the substrate is not in the DB, 'not in DB' is added to the three
        # columns in db_links dict
        if len(query_res) == 0:
            for key in db_links:
                db_links[key].append(not_in_db)
        else:
            # dictionary containing unique substrates, phosphosites and kinases
            # (or None) retrieved by query for data frame row
            in_row = {}
            # iterate subs/phos/kin tuples in query_res
            for subs_phos_kin_trio in query_res:
                # iterate through each element in len(3) tuple
                for instance in subs_phos_kin_trio:
                    # ignore if None
                    if instance:
                        # compare to entries in db_links to determine to which
                        # column values should map
                        for class_name in db_links:
                            if isinstance(instance, class_name):
                                # name of key attr for current class
                                key_attr = db_key_attrs[class_name]
                                # get key value for instance
                                instance_key = getattr(instance, key_attr)
                                # create set of unique key values for class
                                new_set = in_row.setdefault(class_name, set())
                                new_set.add(instance_key)

            # append the new values to the columns dict db_links
            for class_name in db_links:
                if class_name in in_row:
                    to_append = in_row[class_name]
                else:
                    to_append = not_in_db
                db_links[class_name].append(to_append)
    # TODO if pd df not converted to flask table, convert list of str into str with ', '.join(list) when appending

    return db_links

#SELECT substrates.subs_accession AS substrates_subs_accession, substrates.subs_gene AS substrates_subs_gene, phosphosites.phos_group_id AS phosphosites_phos_group_id, phosphosites.phos_modified_residue AS phosphosites_phos_modified_residue, kinases.kin_accession AS kinases_kin_accession, kinases.kin_gene AS kinases_kin_gene FROM substrates LEFT OUTER JOIN phosphosites ON substrates.subs_accession = phosphosites.phos_in_substrate LEFT OUTER JOIN kinases_phosphosites ON phosphosites.phos_group_id = kinases_phosphosites.phos_group_id LEFT OUTER JOIN kinases ON kinases.kin_accession = kinases_phosphosites.kin_accession WHERE substrates.subs_gene = 'RBBP6' AND (phosphosites.phos_modified_residue = 'S770' OR phosphosites.phos_modified_residue IS NULL)