from ckanext.vocabulary_services import model


def vocabulary_service_create(context, data_dict):
    # @TODO: Check access
    session = context['session']

    service = model.VocabularyService(
        type=data_dict.get('type', ''),
        name=data_dict.get('name', ''),
        uri=data_dict.get('uri', ''),
        update_frequency=data_dict.get('update_frequency', ''),
    )

    session.add(service)
    session.commit()

#    return cmt.as_dict()
    return True


def vocabulary_service_term_create(context, data_dict):
    # @TODO: Check access
    session = context['session']

    term = model.VocabularyServiceTerm(
        vocabulary_service_id=data_dict.get('vocabulary_service_id', ''),
        label=data_dict.get('label', ''),
        uri=data_dict.get('uri', '')
    )

    session.add(term)
    session.commit()

    return True
