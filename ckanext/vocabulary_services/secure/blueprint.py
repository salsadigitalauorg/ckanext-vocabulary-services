import ckan.model as model
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.uploader as uploader
import logging
import os
import ckan.plugins.toolkit as toolkit
import mimetypes

from ckan.common import request, c
from ckan.logic import clean_dict, parse_params, tuplize_dict
from ckan.plugins.toolkit import h, render
from ckanext.vocabulary_services import helpers as vocabulary_services_helpers
from ckanext.vocabulary_services.secure import crypt, helpers
from flask import Blueprint
from ckan.views.api import _finish_ok
from pprint import pformat

log = logging.getLogger(__name__)

secure_vocabulary_services = Blueprint('secure_vocabulary_services', __name__, url_prefix=u'/ckan-admin')


def secure_upload():
    vocabulary_services_helpers.check_access({})

    config = helpers.load_secure_vocabularies_config()

    if request.method == 'POST':
        try:
            # The logic for this is based on the following CKAN core logic from:
            #   views/admin.py -> ConfigView -> post
            #   logic/action/update.py -> config_option_update
            req = request.form.copy()
            req.update(request.files.to_dict())
            data_dict = clean_dict(
                dict_fns.unflatten(
                    tuplize_dict(
                        parse_params(req))))

            original_filename = data_dict.get('file_upload').filename
            upload = uploader.get_uploader('secure_csv')
            upload.update_data_dict(data_dict, None, 'file_upload', None)

            # Check The file format is CSV
            # TODO: Check the CSV file has the correct header, compare with the fields in config
            if upload.upload_field_storage.mimetype not in ['text/csv', 'application/vnd.ms-excel']:
                log.debug('Secure upload file mimetype {0} for {1}'.format(upload.upload_field_storage.mimetype, upload.filename))
                raise Exception('Invalid file type "{}". Only "text/csv" files are allowed'.format(upload.upload_field_storage.mimetype))

            max_file_upload_size = int(toolkit.config.get('ckanext.secure_vocabularies.max_file_upload_size', 10))
            upload.upload(max_file_upload_size)

            filename = data_dict.get('filename', None)

            if filename:
                storage_path = upload.storage_path
                uploaded_filepath = upload.filepath

                filepath = os.path.join(storage_path, filename)

                # Delete any existing point-of-contact.csv file
                try:
                    os.remove(filepath)
                except:
                    pass

                # Rename the file to point-of-contact.csv
                os.rename(uploaded_filepath, filepath)

                # Encrypt the file
                # @TODO: Load the key from environment variable set via Lagoon GraphQL API
                # @TODO: For now there is no encryption required until the client verifies what encryption is required
                # crypt.encrypt(filepath, crypt.load_key())

                # @TODO: Remove the temporary file? I don't know if it exists, or if we can?

                h.flash_success('{} successfully uploaded and encrypted.'.format(original_filename))

        except Exception as e:
            h.flash_error(str(e))

    return render('vocabulary/secure_upload.html',
                  extra_vars={
                      'config': config,
                      'data': {},
                      'errors': {},
                  })


def secure_vocabulary_search(vocabulary_name):
    try:
        context = {
            'model': model,
            'user': toolkit.g.user,
            'auth_user_obj': toolkit.g.userobj
        }
        toolkit.check_access(u'package_create', context)
    except toolkit.NotAuthorized:
        toolkit.abort(403, toolkit._('Not authorized'))

    alt_search_display = True if request.args.get('alt', False) else False
    query = request.args.get('incomplete', '')
    limit = request.args.get('limit', 10)
    search_dict = {'vocabulary_name': vocabulary_name, 'query': query, 'limit': limit, 'alt_search_display' : alt_search_display}

    if not query:
        return _finish_ok({})

    result = toolkit.get_action('get_secure_vocabulary_search')({}, search_dict)
    if not result:
        return _finish_ok({})

    result_set = {'ResultSet': {u'Result': result}}

    return _finish_ok(result_set)


secure_vocabulary_services.add_url_rule(u'/vocabulary-services/secure', methods=[u'GET', u'POST'],
                                        view_func=secure_upload)
secure_vocabulary_services.add_url_rule(u'/vocabulary-services/secure-autocomplete/<vocabulary_name>', methods=[u'GET', u'POST'],
                                        view_func=secure_vocabulary_search)
