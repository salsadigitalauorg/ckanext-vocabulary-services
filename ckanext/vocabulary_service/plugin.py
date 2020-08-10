import blueprint
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import helpers

from ckanext.vocabulary_service.logic.action import get, create


class VocabularyServicePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)

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
            'vocabulary_service_create': create.vocabulary_service_create,
            'vocabulary_service_term_create': create.vocabulary_service_term_create,
        }

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_vocabulary_service_types': helpers.get_vocabulary_service_types,
            'get_vocabulary_service_update_frequencies': helpers.get_vocabulary_service_update_frequencies
        }
