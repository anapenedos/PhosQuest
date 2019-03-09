# standard imports
from sqlalchemy import and_, or_
from sqlalchemy.orm import Load
from sqlalchemy.inspection import inspect

# project imports
from PhosphoQuest_app.data_access.db_sessions import create_sqlsession
from PhosphoQuest_app.data_access.sqlalchemy_declarative import Kinase, \
    Substrate, Phosphosite, kinases_phosphosites_table
from PhosphoQuest_app.data_access.class_functions import get_classes_key_attrs


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
    # 'Substrate Entry in DB': [{'ACC1'}, 'not in DB', ...] accessions are stings
    # 'Phosphosite Entry in DB': [{id1}, 'not in DB', ...] ids are integers
    # 'Associated Kinases': [{'ACCa', 'ACCb'}, 'not in DB', ...]
    db_links = {Substrate: [],
                Phosphosite: [],
                Kinase: []}

    # create dictionary for kinase-centric analysis data frame
    # Kinase column contains single kinase accession per line
    # User substrates column contains multiple GENE_site strings for each
    # kinase
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
                        # if an instance of substrate/phosphosite/kinase is
                        # found add it to appropriate column in db_links
                        for class_name in db_links:
                            # compare to entries in db_links to determine to
                            # which column values should map
                            if isinstance(instance, class_name):
                                # name of key attr for current class
                                key_attr = db_key_attrs[class_name]
                                # get key value for instance
                                instance_key = getattr(instance, key_attr)
                                # create set of unique key values for class
                                new_set = in_row.setdefault(class_name, set())
                                new_set.add(instance_key)
                        # if the instance is a kinase, add substrate gene and
                        # residue to that kinases entry in kin_to_ud dict
                        if isinstance(instance, Kinase):
                            kin_acc = instance.kin_accession
                            new_set = kin_to_ud.setdefault(kin_acc, set())
                            new_set.add((gene, residue))

            # append the new values to the columns dict db_links
            for class_name in db_links:
                if class_name in in_row:
                    to_append = in_row[class_name]
                else:
                    to_append = not_in_db
                db_links[class_name].append(to_append)

    # rename db_links keys to present as str
    for col in db_links:
        new_name = col.__name__ + ' DB links'
        db_links[new_name] = db_links.pop(col)

    return db_links, kin_to_ud