import csv
import logging
import os

from ckanext.vocabulary_services.secure import crypt, helpers
from ckan.common import config

log = logging.getLogger(__name__)


def secure_vocabulary_record(context, data_dict):
    results = []

    vocabulary_name = data_dict.get('vocabulary_name', None)
    query = data_dict.get('query', '').lower()

    # Exit early if we don't have what we need to continue
    if not vocabulary_name or len(query) < 1:
        return results

    try:
        secure_vocab_config = helpers.load_secure_vocabulary_config(vocabulary_name)

        if secure_vocab_config and 'filename' in secure_vocab_config:
            secure_filepath = helpers.get_secure_filepath(secure_vocab_config.get('filename', None))

            # Load the decrypted CSV data
            rows = crypt.decrypted_csv_data(secure_filepath, crypt.load_key())

            csv_rows = csv.reader(rows)

            # Always assume the first row of the CSV file is the headers
            headers = next(csv_rows)

            # When looking up a secure CSV row for display - we only want to
            # search on a single field - which is specific in "lookup_field" in .json config
            lookup_field_index = headers.index(secure_vocab_config.get('lookup_field', 0))

            # Create a dict of the fields that should be returned for each result
            # This is based on the 'display_fields' property in the .json config file
            # The dict matches the field names to their position in the CSV header row
            display_fields = {}
            for field in secure_vocab_config.get('display_fields'):
                display_fields[headers.index(field)] = field

            for row in csv_rows:
                if query in row[lookup_field_index].lower():
                    # Restrict what values are returned for the result based on .json config
                    result_dict = {value:row[key] for key, value in display_fields.items()}
                    results.append(result_dict)

            log.error(results)

    except Exception as e:
        print(log.error(e))

    return results
