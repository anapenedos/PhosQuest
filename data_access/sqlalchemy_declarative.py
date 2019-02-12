from sqlalchemy import create_engine, \
                       ForeignKey, Table, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os


# initiates a base sqlalchemy class that handles python<>SQLite "translation"
Base = declarative_base()


# join tables
kinases_inhibitors_table = Table(
    'kinases_inhibitors', Base.metadata,
    Column('kin_accession', String,
           ForeignKey('kinases.kin_accession')),
    Column('inhib_pubchem_cid', Integer,
           ForeignKey('inhibitors.inhib_pubchem_cid'))
)

kinases_phosphosites_table = Table(
    'kinases_phosphosites', Base.metadata,
    Column('kin_accession', String, ForeignKey('kinases.kin_accession')),
    Column('phos_group_id', String, ForeignKey('phosphosites.phos_group_id'))
)


class Kinase(Base):
    """
    Defines a Kinase class mapping to 'kinases' table.
    Data source: PhosphoSitePlus file export Kinase_Substrate_Dataset
    Data source imported to data frame: kin_sub_human
    """
    __tablename__ = 'kinases'

    # kinase accession number is the primary key of kinases table
    kin_accession = Column(String, primary_key=True)
    # kinase short name as impported from PhosphoSitePlus kinase_substrate
    # dataset
    kin_short_name = Column(String)
    # kinase full name (non-abbreviated) as obtained from API
    kin_full_name = Column(String)
    # gene encoding the kinase
    kin_gene = Column(String)
    # organism where kinase is encoded
    # in the first instance of the DB, only human kinases are included
    kin_organism = Column(String)
    # cellular location of the kinase
    kin_cellular_location = Column(String, ForeignKey('locations.loc_name'))
    # kinase family to which the kinase belongs
    kin_family = Column(String)

    # setting up relationships
    # many-to-one 'kinases' <> 'locations' tables
    kin_located = relationship('Location', back_populates='kin_in_loc')
    # many-to-many 'kinases' <> 'inhibitors' tables
    kin_inhibitors = relationship('Inhibitor',
                                  secondary=kinases_inhibitors_table,
                                  back_populates='inhib_target_kinases')
    # many-to-many 'kinases' <> 'phosphosites' tables
    kin_phosphorylates = relationship('Phosphosite',
                                      secondary=kinases_phosphosites_table,
                                      back_populates='phosphorylated_by')

    def __repr__(self):
        return "<Kinase(accession='%s', short name='%s', full name='%s', " \
                       "gene='%s', organism='%s', cellular location='%s', " \
                       "family='%s')>" \
               % (self.kin_accession, self.kin_short_name, self.kin_full_name,
                  self.kin_gene, self.kin_organism, self.kin_cellular_location,
                  self.kin_family)


class Substrate(Base):
    """
    Defines a Substrate class mapping to 'substrates' table.
    Data sources: PhosphositePlus file exports
                - Kinase_Substrate_Dataset
                - Phosphorylation_site_dataset
                - Regulatory_sites
    Data sources imported to data frames:
                - kin_sub_human
                - phos_sites_human
                - reg_sites_human
    """
    __tablename__ = 'substrates'

    # substrate accession number is the primary key of the substrates table
    subs_accession = Column(String, primary_key=True)
    # substrate short name as imported from the PhosphoSitePlus datasets
    subs_short_name = Column(String)
    # substrate full name as obtained from API
    subs_full_name = Column(String)
    # substrate protein type
    subs_protein_type = Column(String)
    # molecular weight (kD) of the substrate
    subs_molec_weight_kd = Column(Float)
    # gene encoding the substrate
    subs_gene = Column(String)
    # chromosomal location of the substrate-encoding gene
    subs_chrom_location = Column(String)
    # substrate organism
    subs_organism = Column(String)

    # setting up relationships
    # one-to-many 'substrates' > 'phosphosites' tables
    subs_sites = relationship('Phosphosite',
                              back_populates='site_in_subs')

    def __repr__(self):
        return "<Substrate(accession='%s', short name='%s', full name='%s', " \
                          "protein type='%s', molecular weight(kD)='%s', " \
                          "gene='%s', chromosomal location='%s')>" \
               % (self.subs_accession, self.subs_short_name,
                  self.subs_full_name, self.subs_protein_type,
                  self.subs_molec_weight_kd, self.subs_gene,
                  self.subs_chrom_location)


class Phosphosite(Base):
    """
    Defines a Phosphosite class mapping to 'phosphosites' table.
    Data source: PhosphoSitePlus file exports
                - Phosphorylation site dataset
                - Regulatory sites
    Data source imported to data frame:
                - phos_sites_human
                - reg_sites_human
    """
    __tablename__ = 'phosphosites'

    # phosphosite group identifier is the primary key of the phosphosites table
    phos_group_id = Column(Integer, primary_key=True)
    # phosphosite modified residue, the amino-acid that is phosphorylated
    phos_modified_residue = Column(String)
    # phosphorylation site, ie, the phosphorylated amino-acid residue plus its
    # flanking 7 amino-acid residues
    phos_site = Column(String)
    # phosphosite domain, the substrate domain where the phosphosite is located
    phos_domain = Column(String)
    # Cell Signalling Technology catalog number(s) of anti-phosphosite
    # antibody(ies)
    phos_cst_catalog_number = Column(String)
    # function(s) of the phosphosite phosphorylation
    phos_p_function = Column(String)
    # process(es) associated with phosphosite phosphorylation
    phos_p_processes = Column(String)
    # protein-protein interaction(s) affected by phosphosite phosphorylation
    phos_prot_interactions = Column(String)
    # non-protein-protein (e.g., protein-DNA) interaction(s) affected by
    # phosphosite phosphorylation
    phos_other_interactions = Column(String)
    # publication references referring to the phosphosite
    phos_bibl_references = Column(String)
    # notes on phosphosite
    phos_notes = Column(String)
    # substrate to which phosphosite belongs
    phos_in_substrate = Column(String, ForeignKey('substrates.subs_accession'))

    # setting up relationships
    # many-to-many 'kinases' <> 'phosphosites' tables
    phosphorylated_by = relationship('Kinase',
                                     secondary=kinases_phosphosites_table,
                                     back_populates='kin_phosphorylates')
    # one-to-many 'substrates' <> 'phosphosites' tables
    site_in_subs = relationship('Substrate',
                                back_populates='subs_sites')
    # one-to-many relationship 'phosphosites' <> 'disease_alterations' tables
    disease_alterations = relationship('DiseaseAlteration',
                                       back_populates='altered_phosphosite')

    def __repr__(self):
        return "<Phosphosite(group ID='%s', modified residue='%s', " \
                            "site +/-7='%s', domain='%s', " \
                            "CST cat number='%s', function='%s', " \
                            "process='%s', " \
                            "protein interactions affected='%s', " \
                            "other interactions affected='%s', " \
                            "references='%s', notes='%s', substrate='%s')>" \
               % (self.phos_group_id, self.phos_modified_residue,
                  self.phos_site, self.phos_domain,
                  self.phos_cst_catalog_number, self.phos_p_function,
                  self.phos_p_processes, self.phos_prot_interactions,
                  self.phos_other_interactions, self.phos_bibl_references,
                  self.phos_notes, self.phos_in_substrate)


class Disease(Base):
    """
    Defines a Disease class mapping to 'diseases' table.
    Data source: PhosphoSitePlus Disease-associated sites dataset
    Data source imported to data frame: dis_sites_human
    """
    __tablename__ = 'diseases'

    # disease name, primary key of diseases table
    dis_name = Column(String, primary_key=True)

    # setting up relationships
    # one-to-many relationship 'diseases' <> 'disease_alterations' tables
    caused_by_alterations = relationship('DiseaseAlteration',
                                         back_populates='altered_in_disease')

    def __repr__(self):
        return "<Disease(name='%s', notes='%s')>" \
              % (self.dis_name, self.dis_notes)


class DiseaseAlteration(Base):
    """
    Defines a DiseaseAlterations class mapping to 'disease_alterations' table.
    Describes the phosphorylation/phosphosite changes associated with disease.
    Data source: PhosphoSitePlus Disease-associated sites dataset
    Data source imported to data frame: dis_sites_human
    """
    __tablename__ = 'disease_alterations'
    # disease alteration associated with disease name
    disalt_disease_name = Column(String,
                                 ForeignKey('diseases.dis_name'),
                                 primary_key=True)
    # disease alteration associated with phosphosite group id
    disalt_phosphosite_id = Column(Integer,
                                   ForeignKey('phosphosites.phos_group_id'),
                                   primary_key=True)
    # disease alteration associated with phosphorylation alteration
    disalt_phos_alteration = Column(String, primary_key=True)
    # publication references referring to the disease-associated alteration
    disalt_bibl_references = Column(String)
    # notes on disease alteration
    disalt_notes = Column(String)

    # setting up relationships
    # one-to-many relationship 'diseases' <> 'disease_alterations' tables
    altered_in_disease = relationship('Disease',
                                      back_populates='caused_by_alterations')
    # many-to-one relationship 'disease_alterations' <> 'phosphosites' tables
    altered_phosphosite = relationship('Phosphosite',
                                       back_populates='disease_alterations')

    def __repr__(self):
        return "<DiseaseAlteration(disease='%s', phosphosite id='%s', " \
                                  "phosphosite/phosphorylation change='%s', " \
                                  "references='%s', note='%s')>" \
              % (self.disalt_disease_name, self.disalt_phosphosite_id,
                 self.disalt_phos_alteration, self.disalt_bibl_references,
                 self.disalt_notes)


class Inhibitor(Base):
    """Defines an Inhibitor class mapping to 'inhibitors' table
    Data source: Medical Research Centre inhibitors database
    Data source imported to data frame: mrc_inhib_source
    """
    __tablename__ = 'inhibitors'

    # inhibitor PubChem compound identifier, primary key of inhibitors table
    inhib_pubchem_cid = Column(Integer, primary_key=True)
    # inhibitor short name
    inhib_short_name = Column(String)
    # inhibitor full name
    inhib_full_name = Column(String)
    # inhibitor brutto (molecular formula)
    inhib_brutto = Column(String)
    # molecular weight of the inhibitor (g/mol)
    inhib_molec_weight = Column(Float)
    # inhibitor SMILE formula
    # Simplified Molecular-Input Line-Entry system: line notation for
    # describing the structure of chemical species using short ASCII strings
    inhib_smile = Column(String)
    # inhibitor IUPAC chemical identifier
    inhib_int_chem_id = Column(String)
    # inhibitor IUPAC chemical identifier key
    inhib_int_chem_id_key = Column(String)
    # publication references referring to the inhibitor
    inhib_bibl_references = Column(String)
    # company selling inhibitor
    inhib_vendor = Column(String)
    # catalog number of the inhibitor in the Vendor's catalog
    inhib_catalog_number = Column(String)

    # setting up relationships
    # many-to-many 'kinases' <> 'inhibitors' tables
    inhib_target_kinases = relationship('Kinase',
                                        secondary=kinases_inhibitors_table,
                                        back_populates='kin_inhibitors')

    def __repr__(self):
        return "<Inhibitor(inhibitor ID='%s', short name='%s', " \
                          "full name='%s', brutto='%s', " \
                          "molec. weight (g/mol)='%s', " \
                          "chemical structure='%s', SMILE='%s', InChI='%s', " \
                          "InChI key='%s', references='%s', vendor='%s', " \
                          "catalog#='%s')>" \
               % (self.inhib_pubchem_cid, self.inhib_short_name,
                  self.inhib_full_name, self.inhib_brutto,
                  self.inhib_molec_weight, self.inhib_chem_structure,
                  self.inhib_smile, self.inhib_int_chem_id,
                  self.inhib_int_chem_id_key, self.inhib_bibl_references,
                  self.inhib_vendor, self.inhib_catalog_number)


class Location(Base):
    """
    Defines an Location class mapping to 'locations' table
    Data source:
    Data source imported to data frame:
    """
    __tablename__ = 'locations'

    # name of the cellular location, primary key of locations table
    loc_name = Column(String, primary_key=True)
    # URL/path to image location
    loc_image_path = Column(String)

    # setting up relationships
    # many-to-one 'kinases' <> 'locations' tables
    kin_in_loc = relationship('Kinase', back_populates='kin_located')

    def __repr__(self):
        return "<Location(name='%s', figure URL='%s')>" \
               % (self.loc_name, self.loc_image_path)


# # Create database tables/schema
# # Create engine that stores data in the local directory's
# # kinases_test.db file.
# # The echo flag sets up SQLAlchemy logging
# db_path = os.path.join('database', 'PhosphoQuest.db')
# engine = create_engine('sqlite:///' + db_path, echo=True)
# # Create all tables
# Base.metadata.create_all(engine)
