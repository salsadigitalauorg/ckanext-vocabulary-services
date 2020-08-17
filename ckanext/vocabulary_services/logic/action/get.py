import logging

from ckanext.vocabulary_services import model

log = logging.getLogger(__name__)


def vocabulary_services(context, data_dict):
    # @TODO: check access / write authentication function
    services = []

    try:
        services = model.VocabularyService.all()
    except Exception as e:
        log.error(str(e))

    return services


def vocabulary_service(context, reference):
    # @TODO: check access / write authentication function
    return model.VocabularyService.get(reference)


def vocabulary_service_terms(context, id):
    # @TODO: check access / write authentication function
    terms = []

    try:
        terms = model.VocabularyServiceTerm.all(id)
    except Exception as e:
        log.error(str(e))

    return terms
