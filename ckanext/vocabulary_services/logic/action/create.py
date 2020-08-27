from ckanext.vocabulary_services.model import VocabularyService, VocabularyServiceTerm
from ckanext.vocabulary_services import helpers, validator


def vocabulary_service_create(context, data_dict):

    helpers.check_access(context)

    session = context['session']

    validator.validate_vocabulary_service(context, data_dict)

    service = VocabularyService(
        type=data_dict.get('type', ''),
        title=data_dict.get('title', ''),
        name=data_dict.get('name', ''),
        uri=data_dict.get('uri', ''),
        update_frequency=data_dict.get('update_frequency', ''),
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
        uri=data_dict.get('uri', '')
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

    if vocabulary_service_id and label and uri:
        # Load any term for the given vocabulary_service.id with matching label OR uri
        existing_term = VocabularyServiceTerm.get_by_label_or_uri(vocabulary_service_id, label, uri)

        if existing_term:
            # Check if something has changed - if so, update it, otherwise skip it...
            if existing_term.label != label or existing_term.uri != uri:
                # Update the term
                existing_term.label = label
                existing_term.uri = uri

                session.add(existing_term)
                session.commit()
        else:
            vocabulary_service_term_create(context, data_dict)

        return True
