import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.vocabulary_services import blueprint, helpers
from ckanext.vocabulary_services.cli import get_commands
from ckanext.vocabulary_services.logic.action import get, create, update


class VocabularyServicesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IClick)

    plugins.toolkit.add_ckan_admin_tab(toolkit.config, 'vocabulary_services.index', 'Vocabulary services', config_var='ckan.admin_tabs', icon=None)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'vocabulary_services')

    # IBlueprint

    def get_blueprint(self):
        return blueprint.vocabulary_services

    # IActions

    def get_actions(self):
        return {
            'get_vocabulary_services': get.vocabulary_services,
            'get_vocabulary_service': get.vocabulary_service,
            'get_vocabulary_service_terms': get.vocabulary_service_terms,
            'get_csiro_vocabulary_terms': get.csiro_vocabulary_terms,
            'get_remote_csv_vocabulary_terms': get.remote_csv_vocabulary_terms,
            'get_vocprez_vocabulary_terms': get.vocprez_vocabulary_terms,
            'vocabulary_service_create': create.vocabulary_service_create,
            'vocabulary_service_edit': update.vocabulary_service_edit,
            'vocabulary_service_delete': update.vocabulary_service_delete,
            'vocabulary_service_term_create': create.vocabulary_service_term_create,
            'vocabulary_service_term_upsert': create.vocabulary_service_term_upsert,
            'update_vocabulary_terms': update.update_vocabulary_terms,
            'update_vocabulary_service_last_processed': update.vocabulary_service_last_processed
        }

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_vocabulary_service_types': helpers.get_vocabulary_service_types,
            'get_vocabulary_service_update_frequencies': helpers.get_vocabulary_service_update_frequencies,
            'scheming_vocabulary_service_choices': helpers.scheming_vocabulary_service_choices,
        }

    # IClick

    def get_commands(self):
        return get_commands()
