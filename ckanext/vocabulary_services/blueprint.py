import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as toolkit

from ckan.common import request
from flask import Blueprint

clean_dict = logic.clean_dict
get_action = toolkit.get_action
h = toolkit.h
parse_params = logic.parse_params
request = toolkit.request
tuplize_dict = logic.tuplize_dict


vocabulary_services = Blueprint('vocabulary_services', __name__, url_prefix=u'/ckan-admin')


def index():
    data = {}
    if request.method == 'POST':
        data = clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(
            request.form))))
        # @TODO: Validate data
        get_action('vocabulary_service_create')({}, data)

    services = get_action('get_vocabulary_services')({}, {})

    return toolkit.render('vocabulary/index.html',
                          extra_vars={
                              'data': data,
                              'errors': {},
                              'services': services
                          })


def refresh(id):
    service = get_action('get_vocabulary_service')({}, id)
    data = [
        {'label': 'Blah', 'uri': 'https://www.google.com/blah'},
        {'label': 'Wah', 'uri': 'https://www.google.com/wah'},
        {'label': 'Haha', 'uri': 'https://www.google.com/haha'},
    ]

    if service:
        for d in data:
            data_dict = {
                'vocabulary_service_id': service.id,
                'label': d['label'],
                'uri': d['uri'],
            }
            get_action('vocabulary_service_term_create')({}, data_dict)

        h.flash_success('Terms in vocabulary refreshed')

    return h.redirect_to('vocabulary_services.index')


def terms(id):
    terms = get_action('get_vocabulary_service_terms')({}, id)

    return toolkit.render('vocabulary/terms.html',
                          extra_vars={
                              'terms': terms,
                          })


vocabulary_services.add_url_rule(u'/vocabulary-services',
                           methods=[u'GET', u'POST'], view_func=index)

vocabulary_services.add_url_rule(u'/vocabulary-service/refresh/<id>', view_func=refresh)

vocabulary_services.add_url_rule(u'/vocabulary-service/terms/<id>', view_func=terms)
