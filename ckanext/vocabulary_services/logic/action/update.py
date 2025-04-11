import logging

from ckan.plugins.toolkit import get_action
from ckanext.vocabulary_services.model import VocabularyService, VocabularyServiceTerm
from ckanext.vocabulary_services import helpers, validator
import datetime


log = logging.getLogger(__name__)


def vocabulary_service_last_processed(context, id):

    helpers.check_access(context)

    vocabulary_service = VocabularyService.get(id)

    if vocabulary_service:
        vocabulary_service.date_last_processed = datetime.datetime.now(datetime.timezone.utc)

def update_vocabulary_terms(context, data_dict):

    helpers.check_access(context)

    id = data_dict.get('id', None)
    uri = data_dict.get('uri', None)
    service_type = data_dict.get('type', None)

    if id and uri and service_type:
        try:
            if service_type == 'sparql_json':
                if get_action('get_sparql_json_vocabulary_terms')(context, data_dict):
                    get_action('update_vocabulary_service_last_processed')(context, id)
                    log.info('Terms in vocabulary refreshed')
            elif service_type == 'remote_csv':
                if get_action('get_remote_csv_vocabulary_terms')(context, data_dict):
                    get_action('update_vocabulary_service_last_processed')(context, id)
                    log.info('Terms in vocabulary refreshed')
            else:
                log.error('Vocabulary service type %s not currently implemented.' % service_type)

        except Exception as e:
            log.error(str(e))


def vocabulary_service_edit(context, data_dict):
    """
    Edit vocabulary service.
    """
    helpers.check_access(context)

    # Set the allow duplicate items value.
    data_dict['allow_duplicate_terms'] = False if not 'allow_duplicate_terms' in data_dict else True
    data_dict['is_hierarchical'] = False if not 'is_hierarchical' in data_dict else True

    # Load vocabulary service.
    vocabulary_service = VocabularyService.get(data_dict['id'])

    # Validate the form values.
    validator.validate_vocabulary_service(context, data_dict, True)

    try:
        if vocabulary_service:
            for key in data_dict:
                setattr(vocabulary_service, key, data_dict[key])

            vocabulary_service.save()
    except Exception as e:
        log.error(str(e))
        raise Exception('Error updating vocabulary service.')

def vocabulary_service_delete(context, id):
    """
    Delete vocabulary service and its term.
    """
    helpers.check_access(context)

    try:
        # Remove terms.
        terms = get_action('get_vocabulary_service_terms')({}, id)

        for term in terms:
            term.delete()
            term.commit()

        vocabulary_service = VocabularyService.get(id)
        vocabulary_service.delete()
        vocabulary_service.commit()
    except Exception as e:
        log.error(e)
        raise Exception("Error deleting vocabulary service.")
