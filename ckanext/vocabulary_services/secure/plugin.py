import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.vocabulary_services.secure import blueprint, helpers
from ckanext.vocabulary_services.secure.logic.action import get


class SecureVocabulariesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    plugins.toolkit.add_ckan_admin_tab(toolkit.config, 'secure_vocabulary_services.secure_upload',
                                       'Secure Vocabularies',
                                       config_var='ckan.admin_tabs', icon=None)

    # IActions

    def get_actions(self):
        return {
            'get_secure_vocabulary_record': get.secure_vocabulary_record,
        } #get_secure_vocabulary_record

    # IBlueprint

    def get_blueprint(self):
        return blueprint.secure_vocabulary_services

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_secure_vocabulary_record': helpers.get_secure_vocabulary_record,
        }
