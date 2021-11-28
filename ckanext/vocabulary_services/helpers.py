import logging

from ckan.lib.base import abort
from ckan.logic import check_access as logic_check_access
from ckan.plugins.toolkit import get_action, h

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


def get_linked_schema_field_options(existing_vocab_services):
    '''
    Get all available options for linked_schema_field,
    any field that already registered in existing_vocab_services
    will be filtered out.
    '''
    package_types = [
        'dataset',
        'dataservice'
    ]
    fields = {
        'dataset__dataset_fields': [],
        'dataservice__dataset_fields': [],
        'dataset__resource_fields': []
    }
    existing_field_names = [service.linked_schema_field for service in existing_vocab_services if len(service.linked_schema_field.strip()) > 0]
    for package_type in package_types:
        schema = h.scheming_get_dataset_schema(package_type)
        dataset_fields = schema.get('dataset_fields', [])

        if package_type == 'dataset':
            resource_fields = schema.get('resource_fields', [])
            fields['dataset__dataset_fields'] = _extract_vocab_field_from_schema(dataset_fields, existing_field_names)
            fields['dataset__resource_fields'] = _extract_vocab_field_from_schema(resource_fields, existing_field_names)
        else:
            fields['dataservice__dataset_fields'] = _extract_vocab_field_from_schema(dataset_fields, existing_field_names)

    return fields


def _extract_vocab_field_from_schema(schema_fields, existing_field_names):
    '''
    Get all fields that has vocabulary_service_name.
    '''
    def extract_vocab(vocab_name, field_name, sf):
        if vocab_name and field_name not in existing_field_names:
            vocab_fields.append({
                'text': sf.get('label'),
                'name': sf.get('vocabulary_service_name'),
                'value': sf.get('field_name')
            })

    vocab_fields = []
    for schema_field in schema_fields:
        extract_vocab(schema_field.get('vocabulary_service_name', False), schema_field.get('field_name', False), schema_field)

        schema_field_groups = schema_field.get('field_group', False)
        if schema_field_groups:
            for schema_field_group in schema_field_groups:
                extract_vocab(schema_field_group.get('vocabulary_service_name', False), schema_field_group.get('field_name', False), schema_field_group)

    # Sort the value.
    return sorted(vocab_fields, key=lambda d: d['text'])
