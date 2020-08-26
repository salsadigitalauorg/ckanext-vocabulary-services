import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df

from ckanext.vocabulary_services import model


def not_empty(key, data, errors):
    """
    Checks if key value is empty or missing
    Copied from ckan_core/ckan/lib/navl/validators.py and removed the raise StopOnError
    """
    value = data.get(key, None)
    if not value or value is df.missing:
        errors[key].append(tk._('Missing value'))


def validate_vocabulary_service(context, vocabulary_data):

    errors = {'title': [], 'name': [], 'type': [], 'uri': [], 'update_frequency': []}

    # Check title
    not_empty('title', vocabulary_data, errors)

    # Check name
    not_empty('name', vocabulary_data, errors)
    # Only check if name exists if there is no not_empty error
    if len(errors.get('name')) == 0 and model.VocabularyService.name_exists(vocabulary_data['name']):
        errors['name'].append(tk._('Name already exists'))

    # Check type
    not_empty('type', vocabulary_data, errors)

    # Check uri
    not_empty('uri', vocabulary_data, errors)
    tk.get_validator('url_validator')('uri', vocabulary_data, errors, context)

    # Check update_frequency
    not_empty('update_frequency', vocabulary_data, errors)

    # remove empty errors that passed
    for key in list(errors.keys()):
        if not errors[key]:
            del errors[key]

    if len(errors) > 0:
        raise tk.ValidationError(errors)
