import logging

from ckan.plugins.toolkit import get_action
from ckanext.vocabulary_services.model import VocabularyService
from ckanext.vocabulary_services import helpers
from datetime import datetime

log = logging.getLogger(__name__)


def vocabulary_service_last_processed(context, id):

    helpers.check_access(context)

    vocabulary_service = VocabularyService.get(id)

    if vocabulary_service:
        vocabulary_service.date_last_processed = datetime.utcnow()
        vocabulary_service.save()


def update_vocabulary_terms(context, data_dict):

    helpers.check_access(context)

    id = data_dict.get('id', None)
    uri = data_dict.get('uri', None)
    service_type = data_dict.get('type', None)

    if id and uri and service_type:
        try:
            if service_type == 'csiro':
                if get_action('get_csiro_vocabulary_terms')(context, data_dict):
                    get_action('update_vocabulary_service_last_processed')(context, id)
                    log.info('Terms in vocabulary refreshed')
            elif service_type == 'vocprez':
                if get_action('get_vocprez_vocabulary_terms')(context, data_dict):
                    get_action('update_vocabulary_service_last_processed')(context, id)
                    log.info('Terms in vocabulary refreshed')
            else:
                log.error('Vocabulary service type %s not currently implemented.' % service_type)

        except Exception as e:
            log.error(str(e))

