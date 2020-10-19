import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.uploader as uploader
import logging
import os

from ckan.common import request
from ckan.logic import clean_dict, parse_params, tuplize_dict
from ckan.plugins.toolkit import h, render
from ckanext.vocabulary_services import helpers as vocabulary_services_helpers
from ckanext.vocabulary_services.secure import crypt, helpers
from flask import Blueprint

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

            upload = uploader.get_uploader('secure_csv')
            upload.update_data_dict(data_dict, None, 'file_upload', None)
            # @TODO: Make this configurable? The default for the upload.upload method is 2MB
            upload.upload(10)

            filename = data_dict.get('filename', None)

            if filename:
                storage_path = upload.storage_path
                uploaded_filepath = upload.filepath

                filepath = os.path.join(storage_path, filename)

                # @TODO: Need to do some validation of the file here before we destroy the existing file, eg.
                # The file format is CSV
                # The CSV file has the correct header row

                # Delete any existing point-of-contact.csv file
                try:
                    os.remove(filepath)
                except:
                    pass

                # Rename the file to point-of-contact.csv
                os.rename(uploaded_filepath, filepath)

                # Encrypt the file
                # @TODO: Load the key from environment variable set via Lagoon GraphQL API
                crypt.encrypt(filepath, crypt.load_key())

                # @TODO: Remove the temporary file? I don't know if it exists, or if we can?

                h.flash_success('{} successfully uploaded and encrypted.'.format(filename))

        except Exception as e:
            h.flash_error(str(e))

    return render('vocabulary/secure_upload.html',
                  extra_vars={
                      'config': config,
                      'data': {},
                      'errors': {},
                  })


secure_vocabulary_services.add_url_rule(u'/vocabulary-services/secure', methods=[u'GET', u'POST'],
                                        view_func=secure_upload)
