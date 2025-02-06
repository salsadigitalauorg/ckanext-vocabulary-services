import datetime

from ckan.model import meta
from ckan.model import types as _types
from sqlalchemy import types, Column, func, ForeignKey
from ckan.model.domain_object import DomainObject
from sqlalchemy import or_, and_

try:
    from ckan.plugins.toolkit import BaseModel
except ImportError:
    # CKAN <= 2.9
    from ckan.model.meta import metadata
    from sqlalchemy.ext.declarative import declarative_base
    BaseModel = declarative_base(metadata=metadata)


class VocabularyService(DomainObject, BaseModel):
    """A VocabularyService object represents an external vocabulary
    used for populating and controlling a metadata schema field"""

    __tablename__ = "vocabulary_service"
    id = Column(types.UnicodeText, primary_key=True, default=_types.make_uuid)
    type = Column(types.UnicodeText, nullable=False)
    title = Column(types.UnicodeText, nullable=False)
    name = Column(types.UnicodeText, nullable=False, unique=True)
    schema = Column(types.UnicodeText, nullable=False)
    linked_schema_field = Column(types.UnicodeText, nullable=False)
    uri = Column(types.UnicodeText, nullable=False)
    update_frequency = Column(types.UnicodeText, nullable=False)
    allow_duplicate_terms = Column(types.Boolean, default=False)
    is_hierarchical = Column(types.Boolean, default=False)
    date_created = Column(types.DateTime, default=datetime.datetime.now(datetime.UTC))
    date_modified = Column(types.DateTime, default=datetime.datetime.now(datetime.UTC))
    date_last_processed = Column(types.DateTime)

    def __init__(self, type=None, title=None, name=None, schema=None, linked_schema_field=None, uri=None, update_frequency=None, allow_duplicate_terms=False, is_hierarchical=False):
        self.type = type
        self.title = title
        self.name = name
        self.schema = schema
        self.linked_schema_field = linked_schema_field
        self.uri = uri
        self.update_frequency = update_frequency
        self.allow_duplicate_terms = allow_duplicate_terms
        self.is_hierarchical = is_hierarchical

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
    def schema_and_linked_schema_field_and_name_exists(cls, schema, linked_schema_field, name):
        '''Returns true if there is a vocabulary with the same schema and linked_schema_field (case insensitive)'''
        query = meta.Session.query(cls)
        return query\
            .filter(func.lower(cls.schema) == func.lower(schema))\
            .filter(func.lower(cls.linked_schema_field) == func.lower(linked_schema_field))\
            .filter(func.lower(cls.name) == func.lower(name))\
            .first() is not None

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


class VocabularyServiceTerm(DomainObject, BaseModel):
    """A VocabularyServiceTerm object represents a term from an external vocabulary
    used for populating and controlling a metadata schema field"""

    __tablename__ = "vocabulary_service_term"
    id = Column(types.UnicodeText, primary_key=True, default=_types.make_uuid)
    vocabulary_service_id = Column(types.UnicodeText, ForeignKey('vocabulary_service.id'), nullable=False)
    label = Column(types.UnicodeText, nullable=False)
    uri = Column(types.UnicodeText, nullable=False)
    broader = Column(types.UnicodeText, nullable=True)
    definition = Column(types.UnicodeText, nullable=True)
    quantity_kind = Column(types.UnicodeText, nullable=True)
    date_created = Column(types.DateTime, default=datetime.datetime.utcnow())
    date_modified = Column(types.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, vocabulary_service_id=None, label=None, uri=None, definition=None, broader=None, quantity_kind=None):
        self.vocabulary_service_id = vocabulary_service_id
        self.label = label
        self.uri = uri
        self.broader = broader
        self.definition = definition
        self.quantity_kind = quantity_kind

    @classmethod
    def get(cls, reference):
        '''Returns a VocabularyServiceTerm object referenced by its id.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        vocabulary_service_term = query.first()

        return vocabulary_service_term

    @classmethod
    def get_by_label_or_uri(cls, vocabulary_service_id, label, uri):
        '''Returns a VocabularyServiceTerm object referenced by its label or uri.'''
        query = meta.Session.query(cls)\
            .filter(cls.vocabulary_service_id == vocabulary_service_id)\
            .filter(or_(func.lower(cls.label) == func.lower(label), func.lower(cls.uri) == func.lower(uri)))
        vocabulary_service_term = query.first()

        return vocabulary_service_term

    @classmethod
    def get_by_label_and_uri(cls, vocabulary_service_id, label, uri):
        '''Returns a VocabularyServiceTerm object referenced by its label and uri.'''
        query = meta.Session.query(cls)\
            .filter(cls.vocabulary_service_id == vocabulary_service_id)\
            .filter(and_(func.lower(cls.label) == func.lower(label), func.lower(cls.uri) == func.lower(uri)))
        vocabulary_service_term = query.first()

        return vocabulary_service_term

    @classmethod
    def get_terms(cls, vocabulary_service_id):
        '''Returns VocabularyServiceTerm objects referenced by vocabulary_service_id.'''
        query = meta.Session.query(cls).filter(cls.vocabulary_service_id == vocabulary_service_id)
        terms = query.all()

        return terms
