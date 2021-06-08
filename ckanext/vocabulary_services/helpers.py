import logging

from ckan.lib.base import abort
from ckan.logic import check_access as logic_check_access
from ckan.plugins.toolkit import get_action
from pprint import pformat

log = logging.getLogger(__name__)


def get_vocabulary_service_types():
    return [
        {'text': 'Remote CSV file', 'value': 'remote_csv'},
        {'text': 'SPARQL + JSON', 'value': 'sparql_json'},
    ]


def get_vocabulary_service_update_frequencies():
    return [
        {'text': 'Daily', 'value': 'daily'},
        {'text': 'Weekly', 'value': 'weekly'},
        {'text': 'Monthly', 'value': 'monthly'},
        {'text': 'Never', 'value': 'never'},
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
                choices.append({'value': term.uri, 'label': term.label, 'title': term.definition})
        except Exception as e:
            log.error(str(e))

    return choices


def check_access(context):
    # `config_option_update` only accessible to sysadmin users
    try:
        logic_check_access('config_option_update', context, {})
    except Exception as e:
        abort(404, 'Not found')


def scheming_vocabulary_service_hierarchical(field):
    """
    Provides a list of terms from a given `vocabulary_service`.`name` with parent and child supports.
    """
    return scheming_vocabulary_service_choices(field)


def render_hierarchical(terms_list):
    def get_top_parents(available_uris):
        return [term for term in terms_list if not term['broader'] in available_uris]

    def get_nodes(term):
        nodes = term.copy()
        children = get_children(term['uri'])
        if children:
            nodes['folder'] = True
            nodes['children'] = [get_nodes(child) for child in children]

        return nodes

    def get_children(broader):
        return [term for term in terms_list if term['broader'] == broader]

    # List available uris.
    available_term_uris = [available_term['uri'] for available_term in terms_list]

    # Find the top parents.
    parents = get_top_parents(available_term_uris)

    # Get children of the parents.
    for parent in parents:
        parent_nodes = get_nodes(parent)
        if parent_nodes.get('children'):
            parent['folder'] = True
            parent['children'] = parent_nodes['children']

    return parents
