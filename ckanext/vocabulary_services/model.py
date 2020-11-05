import datetime

from ckan.model import meta
from ckan.model import types as _types
from sqlalchemy import types, Column, Table, func, ForeignKey
from ckan.model.domain_object import DomainObject
from sqlalchemy.orm import relation
from sqlalchemy import or_


vocabulary_service_table = Table('vocabulary_service', meta.metadata,
                                 Column('id', types.UnicodeText,
                                        primary_key=True,
                                        default=_types.make_uuid),
                                 Column('type', types.UnicodeText,
                                        nullable=False),
                                 Column('title', types.UnicodeText,
                                        nullable=False),
                                 Column('name', types.UnicodeText,
                                        nullable=False,
                                        unique=True),
                                 Column('uri', types.UnicodeText,
                                        nullable=False),
                                 Column('update_frequency', types.UnicodeText,
                                        nullable=False),
                                 Column('allow_duplicate_terms', types.Boolean,
                                        default=False),
                                 Column('date_created', types.DateTime,
                                        default=datetime.datetime.utcnow()),
                                 Column('date_modified', types.DateTime,
                                        default=datetime.datetime.utcnow()),
                                 Column('date_last_processed', types.DateTime),
                                 )

vocabulary_service_term_table = Table('vocabulary_service_term', meta.metadata,
                                      Column('id', types.UnicodeText,
                                             primary_key=True,
                                             default=_types.make_uuid),
                                      Column('vocabulary_service_id', types.UnicodeText,
                                             ForeignKey('vocabulary_service.id'), nullable=False),
                                      Column('label', types.UnicodeText,
                                             nullable=False),
                                      Column('uri', types.UnicodeText,
                                             nullable=False),
                                      Column('definition', types.UnicodeText,
                                             nullable=False),
                                      Column('date_created', types.DateTime,
                                             default=datetime.datetime.utcnow()),
                                      Column('date_modified', types.DateTime,
                                             default=datetime.datetime.utcnow()),
                                      )


class VocabularyService(DomainObject):
    """A VocabularyService object represents an external vocabulary
    used for populating and controlling a metadata schema field"""

    def __init__(self, type=None, title=None, name=None, uri=None, update_frequency=None, allow_duplicate_terms=False):
        self.type = type
        self.title = title
        self.name = name
        self.uri = uri
        self.update_frequency = update_frequency
        self.allow_duplicate_terms = allow_duplicate_terms

    @classmethod
    def get(cls, reference):
        '''Returns a VocabularyService object referenced by its id or name.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        vocabulary_service = query.first()
        if vocabulary_service is None:
            vocabulary_service = cls.by_name(reference)
        return vocabulary_service

    @classmethod
    def all(cls):
        """
        Returns all vocabularies.
        """
        q = meta.Session.query(cls)

        return q.order_by(cls.name).all()

    @classmethod
    def name_exists(cls, name):
        '''Returns true if there is a vocabulary with the same name (case insensitive)'''
        query = meta.Session.query(cls)
        return query.filter(func.lower(cls.name) == func.lower(name)).first() is not None

    @classmethod
    def get_by_name(cls, name):
        '''Returns true if there is a vocabulary with the same name (case insensitive)'''
        query = meta.Session.query(cls)
        return query.filter(func.lower(cls.name) == func.lower(name)).all()

    @classmethod
    def is_allow_duplicate_terms(cls, reference):
        '''Return True if allow_duplicate_terms'''
        query = meta.Session.query(cls)
        return query.filter(cls.allow_duplicate_terms == True).filter(cls.id == reference).first() is not None

class VocabularyServiceTerm(DomainObject):
    """A VocabularyServiceTerm object represents a term from an external vocabulary
    used for populating and controlling a metadata schema field"""

    def __init__(self, vocabulary_service_id=None, label=None, uri=None):
        self.vocabulary_service_id = vocabulary_service_id
        self.label = label
        self.uri = uri

    @classmethod
    def get(cls, reference):
        '''Returns a VocabularyServiceTerm object referenced by its id.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        vocabulary_service_term = query.first()

        return vocabulary_service_term

    @classmethod
    def get_by_label_or_uri(cls, vocabulary_service_id, label, uri):
        '''Returns a VocabularyServiceTerm object referenced by its id.'''
        query = meta.Session.query(cls)\
            .filter(cls.vocabulary_service_id == vocabulary_service_id)\
            .filter(or_(cls.label == label, cls.uri == uri))
        vocabulary_service_term = query.first()

        return vocabulary_service_term

    @classmethod
    def get_by_uri(cls, vocabulary_service_id, uri):
        '''Returns a VocabularyServiceTerm object referenced by its uri.'''
        query = meta.Session.query(cls)\
            .filter(cls.vocabulary_service_id == vocabulary_service_id)\
            .filter(cls.uri == uri)
        vocabulary_service_term = query.first()

        return vocabulary_service_term


meta.mapper(VocabularyService, vocabulary_service_table, properties={
    'terms': relation(lambda: VocabularyServiceTerm, order_by=lambda: VocabularyServiceTerm.label)
})
meta.mapper(VocabularyServiceTerm, vocabulary_service_term_table)
