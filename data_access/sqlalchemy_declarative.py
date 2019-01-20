from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# initiates a Base sqlalchemy class that handles python<>SQLite "translation"
Base = declarative_base()


class Kinase(Base):
    """Defines a Kinase class mapping to 'kinases' table"""
    __tablename__ = 'kinases'

    kin_acc_num = Column(String(20), primary_key=True)  # accession number
    kin_name = Column(String(50))  # TODO check max len of fields
    kin_gene = Column(String(20))
    kin_prot = Column(String(20))  # protein
    kin_org = Column(String(150))  # organism
    kin_loc = Column(String(150))  # location
    kin_fam = Column(String(150))  # family

    def __repr__(self):
        return "<Kinase(accession='%s', name='%s', gene='%s', protein='%s'," \
                       "organism='%s', location='%s', family='%s')>" \
               % (self.kin_acc_num, self.kin_name, self.kin_gene,
                  self.kin_prot, self.kin_org, self.kin_loc, self.kin_fam)


class Substrate(Base):
    """Defines a Substrate class mapping to 'substrates' table"""
    __tablename__ = 'substrates'

    subs_acc_num = Column(String(20), primary_key=True)  # accession number
    subs_name = Column(String(20))
    subs_gene_id = Column(Integer)
    subs_gene = Column(String(20))
    # TODO substrate protein?
    subs_org = Column(String(150))  # organism
    subs_mod_res = Column(String(150))  # modified residue TODO integer?
    subs_domain = Column(String(150))  # modified domain
    subs_ab = Column(String(20))  # CST catalog number TODO integer?

    def __repr__(self):
        return "<Substrate(accession='%s', name='%s', gene ID='%s', " \
                          "gene='%s', organism='%s', modified residue='%s'" \
                          "domain='%s', antibody='%s')>" \
               % (self.subs_acc_num, self.subs_name, self.subs_gene_id,
                  self.subs_gene, self.subs_org, self.subs_mod_res,
                  self.subs_domain, self.subs_ab)


class Phosphosite(Base):
    """Defines a Phosphosite class mapping to 'phosphosites' table"""
    __tablename__ = 'phosphosites'

    phos_cat_id = Column(Integer, primary_key=True)  # category ID TODO str?
    phos_site = Column(String(20))  # site +/- 7
    phos_genomic_loc = Column(String(150))  # genomic location

    def __repr__(self):
        return "<Phosphosite(category ID='%s', site +/-7='%s', " \
                            "genomic location='%s')>" \
               % (self.phos_cat_id, self.phos_site, self.phos_genomic_loc)


class Inhibitor(Base):
    """Defines an Inhibitor class mapping to 'inhibitors' table"""
    __tablename__ = 'inhibitors'

    inhib_id = Column(Integer, primary_key=True)  # inhibitor ID
    inhib_chem_struct = Column(String(20))  # chemical structure

    def __repr__(self):
        return "<Inhibitor(inhibitor ID='%s', chemical structure='%s')>" \
               % (self.inhib_id, self.inhib_chem_struct)


class Location(Base):
    """Defines an Location class mapping to 'locations' table"""
    __tablename__ = 'locations'

    loc_id = Column(Integer, primary_key=True)  # location ID
    loc_name = Column(String(20))
    loc_fig_url = Column(String(300))  # URL to image of location

    def __repr__(self):
        return "<Location(location ID='%s', name='%s', figure URL='%s')>" \
               % (self.loc_id, self.loc_name, self.loc_fig_url)




# Create engine that stores data in the local directory's
# kinases_test.db file.
# The echo flag sets up SQLAlchemy logging
# TODO rmv echo when functional
# TODO replace by final db file for release
engine = create_engine('sqlite:///database/kinases_test.db', echo=True)
# Create all tables
Base.metadata.create_all(engine)
