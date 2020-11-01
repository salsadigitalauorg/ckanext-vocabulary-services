import json
import os
import logging

from ckan.plugins.toolkit import abort, get_action, config

log = logging.getLogger(__name__)


def load_secure_vocabularies_config():
    """
    Load some config info from a json file
    """
    try:
        json_config = config.get('ckanext.secure_vocabularies.json_config')
        with open(json_config) as json_data:
            d = json.load(json_data)
            return d
    except Exception as e:
        abort(403, "Secure vocabularies configuration file not found.")


def load_secure_vocabulary_config(vocabulary_name):
    secure_vocabulary_config = [
        x for x in load_secure_vocabularies_config() if x.get('name', None) == vocabulary_name
    ]

    return secure_vocabulary_config[0] if secure_vocabulary_config[0] else {}


def get_secure_filepath(filename):
    return os.path.join(
        config.get('ckan.storage_path'),
        # Because we are using the standard CKAN uploader class - "storage/uploads" is the path
        'storage',
        'uploads',
        config.get('ckanext.secure_vocabularies.secure_dir', 'secure_csv'),
        filename
    )


def get_secure_vocabulary_record(vocabulary_name, query):
    if get_secure_vocabulary_lookup_field(vocabulary_name):
        return get_action('get_secure_vocabulary_record')({}, {'vocabulary_name': vocabulary_name, 'query': query})


def get_secure_vocabulary_record_label(vocabulary_name, query):
    # Query could be a free text value and will not be found in the get_secure_vocabulary_record lookup
    label = query
    if get_secure_vocabulary_lookup_field(vocabulary_name):
        secure_vocabulary_record = get_secure_vocabulary_record(vocabulary_name, query)
        if secure_vocabulary_record:
            search_display_fields = load_secure_vocabulary_config(vocabulary_name).get('search_display_fields', {})
            label = search_display_fields.get('name', '').format(**secure_vocabulary_record)

    return label


def get_secure_vocabulary_lookup_field(vocabulary_name):
    secure_vocabulary_config = load_secure_vocabulary_config(vocabulary_name)
    return secure_vocabulary_config.get('lookup_field', False)
