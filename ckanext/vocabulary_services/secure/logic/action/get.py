import csv
import logging
import ckan.plugins.toolkit as toolkit
import ckan.authz as authz

from ckanext.vocabulary_services.secure import crypt, helpers


log = logging.getLogger(__name__)


def secure_vocabulary_record(context, data_dict):
    if authz.auth_is_anon_user(context):
        return {'success': False, 'msg': toolkit._('Not authorized')}

    result = {}
    vocabulary_name = data_dict.get('vocabulary_name', None)
    query = data_dict.get('query', '').lower()

    # Exit early if we don't have what we need to continue
    if not vocabulary_name or len(query) < 1:
        return result

    try:
        secure_vocab_config = helpers.load_secure_vocabulary_config(vocabulary_name)

        if secure_vocab_config and 'filename' in secure_vocab_config:
            secure_filepath = helpers.get_secure_filepath(secure_vocab_config.get('filename', None))

            # Load the decrypted CSV data
            # TODO: Decrypted_csv_data once client confirms encryption required
            # rows = crypt.decrypted_csv_data(secure_filepath, crypt.load_key())
            # csv_rows = csv.DictReader(rows))

            lookup_field = secure_vocab_config.get('lookup_field', '')
            display_fields = secure_vocab_config.get('display_fields', '')

            csv_rows = csv.DictReader(open(secure_filepath))
            for row in map(dict, csv_rows):
                if row[lookup_field] == query:
                    result = {field: row[field] for field in display_fields}
                    break

    except Exception as e:
        log.error(e)

    return result


def secure_vocabulary_search(context, data_dict):
    if not authz.has_user_permission_for_some_org(context.get('user'), 'create_dataset'):
        return {'success': False, 'msg': toolkit._('Not authorized')}

    results = []
    vocabulary_name = data_dict.get('vocabulary_name', None)
    query = data_dict.get('query', '').lower()
    limit = data_dict.get('limit', 10)

    # Exit early if we don't have what we need to continue.
    # Minimum of 3+ characters must be entered before searching
    if not vocabulary_name or len(query) < 3:
        return results

    try:
        secure_vocab_config = helpers.load_secure_vocabulary_config(vocabulary_name)

        if secure_vocab_config and 'filename' in secure_vocab_config:
            secure_filepath = helpers.get_secure_filepath(secure_vocab_config.get('filename', None))

            # Load the decrypted CSV data
            # TODO: Decrypted_csv_data once client confirms encryption required
            # rows = crypt.decrypted_csv_data(secure_filepath, crypt.load_key())
            # csv_rows = csv.DictReader(rows))

            search_display_fields = secure_vocab_config.get('search_display_fields')
            search_fields = secure_vocab_config.get('search_fields')

            csv_rows = csv.DictReader(open(secure_filepath))
            for row in map(dict, csv_rows):
                # Check to see if result limit has been reached
                if len(results) >= limit:
                    break
                for search_field in search_fields:
                    if query in row[search_field].lower():
                        result_dict = {
                            "value": search_display_fields.get('value', '').format(**row),
                            "name": search_display_fields.get('name', '').format(**row)
                        }
                        # Check if result already exists before adding it to results list
                        if not next((result for result in results if result == result_dict), None):
                            results.append(result_dict)
                            # Row has been added to results so move onto the next row
                            break

    except Exception as e:
        log.error(e)

    return results
