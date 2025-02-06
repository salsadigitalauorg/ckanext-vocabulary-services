import logging
import datetime

from ckanext.vocabulary_services.model import VocabularyService, VocabularyServiceTerm
from ckanext.vocabulary_services import helpers, validator


log = logging.getLogger(__name__)


def vocabulary_service_create(context, data_dict):

    helpers.check_access(context)

    session = context["session"]

    validator.validate_vocabulary_service(context, data_dict)

    allow_duplicate_terms = True if data_dict.get("allow_duplicate_terms") else False
    is_hierarchical = True if data_dict.get("is_hierarchical") else False

    service = VocabularyService(
        type=data_dict.get("type", ""),
        title=data_dict.get("title", ""),
        name=data_dict.get("name", ""),
        schema=data_dict.get("schema", ""),
        linked_schema_field=data_dict.get("linked_schema_field", ""),
        uri=data_dict.get("uri", ""),
        update_frequency=data_dict.get("update_frequency", ""),
        allow_duplicate_terms=allow_duplicate_terms,
        is_hierarchical=is_hierarchical,
    )

    session.add(service)
    session.commit()

    return True


def vocabulary_service_term_create(context, data_dict):

    helpers.check_access(context)

    session = context["session"]

    term = VocabularyServiceTerm(
        vocabulary_service_id=data_dict.get("vocabulary_service_id", ""),
        label=data_dict.get("label", ""),
        uri=data_dict.get("uri", ""),
        broader=data_dict.get("broader", ""),
        definition=data_dict.get("definition", ""),
        quantity_kind=data_dict.get("quantity_kind", ""),
    )

    session.add(term)
    session.commit()

    return True


def vocabulary_service_term_upsert(context, data_dict):

    helpers.check_access(context)

    session = context["session"]

    vocabulary_service_id = data_dict.get("vocabulary_service_id", None)
    label = data_dict.get("label", None)
    uri = data_dict.get("uri", None)
    definition = data_dict.get("definition", None)
    quantity_kind = data_dict.get("quantity_kind", None)
    broader = data_dict.get("broader", None)

    if vocabulary_service_id and label and uri:
        existing_term = None
        allow_duplicate_terms = VocabularyService.is_allow_duplicate_terms(
            vocabulary_service_id
        )
        if allow_duplicate_terms:
            # Load any term for the given vocabulary_service.id with matching label AND uri
            existing_term = VocabularyServiceTerm.get_by_label_and_uri(
                vocabulary_service_id, label, uri
            )
        else:
            # Load any term for the given vocabulary_service.id with matching label OR uri
            existing_term = VocabularyServiceTerm.get_by_label_or_uri(
                vocabulary_service_id, label, uri
            )

        if existing_term:
            # Check if something has changed - if so, update it, otherwise skip it...
            if (
                existing_term.label != label
                or existing_term.uri != uri
                or existing_term.definition != definition
                or existing_term.broader != broader
                or existing_term.quantity_kind != quantity_kind
            ):
                # Update the term
                existing_term.label = label
                existing_term.uri = uri
                existing_term.broader = broader
                existing_term.definition = definition
                existing_term.quantity_kind = quantity_kind
                existing_term.date_modified = datetime.datetime.now(datetime.UTC)

                session.add(existing_term)
                session.commit()
        else:
            vocabulary_service_term_create(context, data_dict)

        return True
