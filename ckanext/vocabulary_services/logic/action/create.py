import logging

from ckanext.vocabulary_services.model import VocabularyService, VocabularyServiceTerm
from ckanext.vocabulary_services import helpers, validator
from datetime import datetime
from pprint import pformat

log = logging.getLogger(__name__)


def vocabulary_service_create(context, data_dict):

    helpers.check_access(context)

    session = context['session']

    validator.validate_vocabulary_service(context, data_dict)

    allow_duplicate_terms = True if data_dict.get('allow_duplicate_terms') else False
    is_hierarchical = True if data_dict.get('is_hierarchical') else False

    service = VocabularyService(
        type=data_dict.get('type', ''),
        title=data_dict.get('title', ''),
        name=data_dict.get('name', ''),
        uri=data_dict.get('uri', ''),
        update_frequency=data_dict.get('update_frequency', ''),
        allow_duplicate_terms=allow_duplicate_terms,
        is_hierarchical=is_hierarchical,
    )

    session.add(service)
    session.commit()

    return True


def vocabulary_service_term_create(context, data_dict):

    helpers.check_access(context)

    session = context['session']

    term = VocabularyServiceTerm(
        vocabulary_service_id=data_dict.get('vocabulary_service_id', ''),
        label=data_dict.get('label', ''),
        uri=data_dict.get('uri', ''),
        definition=data_dict.get('definition', '')
    )

    session.add(term)
    session.commit()

    return True


def vocabulary_service_term_upsert(context, data_dict):

    helpers.check_access(context)

    session = context['session']

    vocabulary_service_id = data_dict.get('vocabulary_service_id', None)
    label = data_dict.get('label', None)
    uri = data_dict.get('uri', None)
    definition = data_dict.get('definition', None)

    if vocabulary_service_id and label and uri:
        existing_term = None

        if VocabularyService.is_allow_duplicate_terms(vocabulary_service_id):
            # Load any term for the given vocabulary_service.id with matching uri
            existing_term = VocabularyServiceTerm.get_by_uri(vocabulary_service_id, uri)
        else:
            # Load any term for the given vocabulary_service.id with matching label OR uri
            existing_term = VocabularyServiceTerm.get_by_label_or_uri(vocabulary_service_id, label, uri)

        if existing_term:
            # If duplicate terms are allowed.
            if VocabularyService.is_allow_duplicate_terms(vocabulary_service_id):
                if (existing_term.label == label) and (existing_term.uri != uri):
                    # If label is the same but uri is different, let's create them.
                    vocabulary_service_term_create(context, data_dict)
                elif (existing_term.label != label or existing_term.definition != definition) and existing_term.uri == uri:
                    # Update the term label if the URI is the same and label different.
                    # Update the term definition if the URI is the same and definition different.
                    existing_term.label = label
                    existing_term.definition = definition
                    existing_term.date_modified = datetime.utcnow()

                    session.add(existing_term)
                    session.commit()
                else:
                    return True
            else:
                # Check if something has changed - if so, update it, otherwise skip it...
                if existing_term.label != label or existing_term.uri != uri or existing_term.definition != definition:
                    # Update the term
                    existing_term.label = label
                    existing_term.uri = uri
                    existing_term.definition = definition
                    existing_term.date_modified = datetime.utcnow()

                    session.add(existing_term)
                    session.commit()
        else:
            vocabulary_service_term_create(context, data_dict)

        return True
