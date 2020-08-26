import logging

from ckan.plugins.toolkit import get_action

log = logging.getLogger(__name__)


def get_vocabulary_service_types():
    return [
        {'text': 'CKAN CSV Resource', 'value': 'ckan_csv'},
        {'text': 'GitHub CSV', 'value': 'github_csv'},
        {'text': 'GSQ VocPrez', 'value': 'vocprez'},
        {'text': 'CSIRO Linked Data Registry', 'value': 'csiro'},
    ]


def get_vocabulary_service_update_frequencies():
    return [
        {'text': 'Daily', 'value': 'daily'},
        {'text': 'Weekly', 'value': 'weekly'},
        {'text': 'Monthly', 'value': 'monthly'},
    ]


def scheming_vocabulary_service_choices(field):
    """
    Provides a list of terms from a given `vocabulary_service`.`name`
    """
    choices = []

    vocabulary_service_name = field.get('vocabulary_service_name', None)
    if vocabulary_service_name:
        try:
            for term in get_action('get_vocabulary_service_terms')({}, vocabulary_service_name):
                choices.append({'value': term.uri, 'label': term.label})
        except Exception as e:
            log.error(str(e))

    return choices
