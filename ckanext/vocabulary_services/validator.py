import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df
import logging

from ckanext.vocabulary_services import model
from ckanext.invalid_uris.helpers import valid_uri

log = logging.getLogger(__name__)
h = tk.h


def not_empty(key, data, errors):
    """
    Checks if key value is empty or missing
    Copied from ckan_core/ckan/lib/navl/validators.py and removed the raise StopOnError
    """
    value = data.get(key, None)
    if not value or value is df.missing:
        errors[key].append(tk._('Missing value'))


def validate_vocabulary_service(context, vocabulary_data, is_update=False):

    errors = {'title': [], 'schema': [], 'linked_schema_field': [], 'name': [], 'type': [], 'uri': [], 'update_frequency': []}

    # Check title
    not_empty('title', vocabulary_data, errors)

    # Check schema
    not_empty('schema', vocabulary_data, errors)

    # Check linked_schema_field.
    not_empty('linked_schema_field', vocabulary_data, errors)
    # Validate if schema field exist.
    schema_name = vocabulary_data.get('schema').split('__')
    schema = h.scheming_get_dataset_schema(schema_name[0])
    schema_fields = schema.get(schema_name[1])
    field_exist = False
    for field in schema_fields:
        if field.get('field_group', False):
            for field_group in field.get('field_group'):
                if field_group.get('field_name') == vocabulary_data.get('linked_schema_field'):
                    field_exist = True
        else:
            if field.get('field_name') == vocabulary_data.get('linked_schema_field'):
                field_exist = True

    if not field_exist:
        errors['linked_schema_field'].append(tk._('Linked schema field not found'))

    # Only check if this combination fields are not already in use.
    schema_and_linked_schema_field_and_name_exists = len(errors.get('linked_schema_field')) == 0 and \
        model.VocabularyService.schema_and_linked_schema_field_and_name_exists(vocabulary_data.get(
            'schema'), vocabulary_data.get('linked_schema_field'), vocabulary_data.get('name'))
    if not is_update and schema_and_linked_schema_field_and_name_exists is None:
        errors['name'].append(tk._('Name already exists'))
        errors['linked_schema_field'].append(tk._('Linked schema field already exists'))
        errors['schema'].append(tk._('Schema already exists'))

    # Check name
    not_empty('name', vocabulary_data, errors)
    # Only check if name exists if there is no not_empty error
    if len(errors.get('name')) == 0 and model.VocabularyService.name_exists(vocabulary_data['name']) and not is_update:
        errors['name'].append(tk._('Name already exists'))

    # Make sure only current vocab is using the same name when edit.
    if len(errors.get('name')) == 0 and is_update:
        vocab_by_name = model.VocabularyService.get_by_name(vocabulary_data['name'])

        if vocab_by_name:
            if len(vocab_by_name) > 1 or vocab_by_name[0].id != vocabulary_data['id']:
                errors['name'].append(tk._('Name already exists'))

    # Check type
    not_empty('type', vocabulary_data, errors)

    # Check uri
    not_empty('uri', vocabulary_data, errors)
    tk.get_validator('url_validator')('uri', vocabulary_data, errors, context)

    # Validate uri.
    valid_uri_resp = valid_uri(vocabulary_data['uri'])
    if not valid_uri_resp.get('valid'):
        errors['uri'].append(tk._('Uri is not valid'))

    # Check update_frequency
    not_empty('update_frequency', vocabulary_data, errors)

    # remove empty errors that passed
    for key in list(errors.keys()):
        if not errors[key]:
            del errors[key]

    if len(errors) > 0:
        raise tk.ValidationError(errors)
