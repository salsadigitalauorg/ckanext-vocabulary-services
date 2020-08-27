import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as toolkit
import logging

from ckan.common import request
from ckanext.vocabulary_services import helpers
from flask import Blueprint

clean_dict = logic.clean_dict
get_action = toolkit.get_action
h = toolkit.h
log = logging.getLogger(__name__)
parse_params = logic.parse_params
request = toolkit.request
tuplize_dict = logic.tuplize_dict

vocabulary_services = Blueprint('vocabulary_services', __name__, url_prefix=u'/ckan-admin')


def index():

    helpers.check_access({})

    try:
        data = {}
        errors = {}
        if request.method == 'POST':
            data = clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(
                request.form))))
            try:
                get_action('vocabulary_service_create')({}, data)
            except toolkit.ValidationError as e:
                log.warn(e)
                errors = e.error_dict
                log.debug(errors)

        services = get_action('get_vocabulary_services')({}, {})

        return toolkit.render('vocabulary/index.html',
                              extra_vars={
                                  'data': data,
                                  'errors': errors,
                                  'services': services
                              })
    except Exception as e:
        log.error(e)
        toolkit.abort(503, str(e))


def refresh(id):

    helpers.check_access({})

    service = get_action('get_vocabulary_service')({}, id)

    if service:
        if service.type == 'csiro':
            log.debug('>>> Attempting to fetch vocabulary from CSIRO service...')
            if get_action('get_csiro_vocabulary_terms')({}, service):
                log.debug('>>> Finished fetching vocabulary from CSIRO service.')
                h.flash_success('Terms in vocabulary refreshed')
            else:
                log.error('>>> ERROR Attempting to fetch vocabulary from CSIRO service')
        elif service.type == 'vocprez':
            log.debug('>>> Attempting to fetch vocabulary from VocPrez service...')
            if get_action('get_vocprez_vocabulary_terms')({}, service):
                log.debug('>>> Finished fetching vocabulary from VocPrez service.')
                h.flash_success('Terms in vocabulary refreshed')
            else:
                log.error('>>> ERROR Attempting to fetch vocabulary from VocPrez service')
        else:
            h.flash_error('Vocabulary service not currently implemented.')

    return h.redirect_to('vocabulary_services.index')


def terms(id):

    helpers.check_access({})

    return toolkit.render('vocabulary/terms.html',
                          extra_vars={
                              'terms': get_action('get_vocabulary_service_terms')({}, id),
                          })


vocabulary_services.add_url_rule(u'/vocabulary-services',
                                 methods=[u'GET', u'POST'], view_func=index)

vocabulary_services.add_url_rule(u'/vocabulary-service/refresh/<id>', view_func=refresh)

vocabulary_services.add_url_rule(u'/vocabulary-service/terms/<id>', view_func=terms)
