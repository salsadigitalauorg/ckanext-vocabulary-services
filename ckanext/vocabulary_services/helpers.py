import logging

from ckan.lib.base import abort
from ckan.logic import check_access as logic_check_access
from ckan.plugins.toolkit import get_action

log = logging.getLogger(__name__)


def get_vocabulary_service_types():
    return [
        {'text': 'Remote CSV file', 'value': 'remote_csv'},
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


def check_access(context):
    # `config_option_update` only accessible to sysadmin users
    try:
        logic_check_access('config_option_update', context, {})
    except Exception as e:
        abort(404, 'Not found')
