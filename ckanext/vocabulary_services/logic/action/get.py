import logging
import requests
import csv
import codecs

from ckan.plugins.toolkit import get_action
from ckanext.vocabulary_services import helpers, model
from pprint import pformat

log = logging.getLogger(__name__)


def vocabulary_services(context, data_dict):

    helpers.check_access({})

    services = []

    try:
        services = model.VocabularyService.all()
    except Exception as e:
        log.error(str(e))

    return services


def vocabulary_service(context, reference):
    return model.VocabularyService.get(reference)


def vocabulary_service_terms(context, name):
    # @TODO: check access / write authentication function
    terms = []

    try:
        data = vocabulary_service(context, name)
        terms = data.terms
    except Exception as e:
        log.error('Vocabulary service name: {0}'.format(name))
        log.error(str(e))

    return terms


def csiro_vocabulary_terms(context, data_dict):
    """
    Query the externally hosted vocabulary and extract the terms out into our internal
    vocabulary service.
    Example:
        http://registry.it.csiro.au/def/isotc211/MD_SpatialRepresentationTypeCode

    This example has multiple output types - for this example we will attempt to use
    the JSON-LD endpoint:

        http://registry.it.csiro.au/def/isotc211/MD_SpatialRepresentationTypeCode?_format=jsonld
    """
    log.debug('>>> Attempting to fetch vocabulary from CSIRO service...')

    service_id = data_dict.get('id', None)
    service_uri = data_dict.get('uri', None)

    if service_id and service_uri:
        try:
            r = requests.get(service_uri)

            log.debug('>>> Request status code: %s' % r.status_code)

            if r.status_code == 200:
                log.debug('>>> Finished fetching vocabulary from CSIRO service.')

                response = r.json()

                # If you open the *?_format=jsonld URI above, you can see that the terms are
                # contained in the '@graph' dict element, and the first item in that list is
                # some metadata about the vocabulary, so we'll skip that for now.
                for i in range(len(response['@graph'])):
                    if i > 0:
                        term = response['@graph'][i]
                        uri = term.get('@id', None)
                        label = term.get('rdfs:label', None)
                        if uri and label:
                            # Create the term in the internal vocabulary service
                            get_action('vocabulary_service_term_upsert')(context, {
                                'vocabulary_service_id': service_id,
                                'label': label,
                                'uri': uri,
                            })
                return True

        except Exception as e:
            log.error('>>> ERROR Attempting to fetch vocabulary from CSIRO service')
            log.error(str(e))

    return False


def vocprez_vocabulary_terms(context, data_dict):
    """
    Query the externally hosted vocabulary and extract the terms out into our internal
    vocabulary service.
    Example:
        https://vocabs.gsq.digital/endpoint?query=PREFIX%20skos%3A%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3ESELECT%3Fconcept%3FprefLabel%20WHERE%7B%3Fconcept%20a%20skos%3AConcept%3Bskos%3AprefLabel%3FprefLabel%3Bskos%3AinScheme%3Chttp%3A%2F%2Flinked.data.gov.au%2Fdef%2Fgsq-dataset-theme%3E.%7Dorder%20by%3FprefLabel&Accept=application/sparql-results+json
    """
    log.debug('>>> Attempting to fetch vocabulary from VocPrez service...')

    service_id = data_dict.get('id', None)
    service_uri = data_dict.get('uri', None)

    if service_id and service_uri:
        try:
            r = requests.get(service_uri)

            log.debug('>>> Request status code: %s' % r.status_code)

            if r.status_code == 200:
                log.debug('>>> Finished fetching vocabulary from VocPrez service.')

                response = r.json()

                # If you open the https://vocabs.gsq.digital... URI above, you can see that the terms are
                # contained in the 'results' dict element, and the 'bindings' element beneath that.
                results = response.get('results', None)
                bindings = results.get('bindings', None)

                if bindings:
                    for binding in bindings:
                        log.debug(binding)
                        concept = binding.get('concept', None)
                        pref_label = binding.get('prefLabel', None)
                        if concept and pref_label:
                            # Create the term in the internal vocabulary service
                            get_action('vocabulary_service_term_upsert')(context, {
                                'vocabulary_service_id': service_id,
                                'label': pref_label['value'],
                                'uri': concept['value'],
                            })
                    return True

        except Exception as e:
            log.error('>>> ERROR Attempting to fetch vocabulary from VocPrez service')
            log.error(str(e))

    return False


def remote_csv_vocabulary_terms(context, data_dict):
    log.debug('>>> Attempting to fetch vocabulary from CKAN CSV...')

    service_id = data_dict.get('id', None)
    service_uri = data_dict.get('uri', None)

    if service_id and service_uri:
        try:
            r = requests.get(service_uri)

            log.debug('>>> Request status code: %s' % r.status_code)

            if r.status_code == 200:
                log.debug('>>> Finished fetching vocabulary from CKAN CSV.')

                response = r.iter_lines()
                reader = csv.DictReader(codecs.iterdecode(response, 'utf-8'))
                rows = list(reader)

                for index in range(len(rows)):
                    label = rows[index].get('label')
                    uri = rows[index].get('uri')
                    if uri and label:
                        # Create the term in the internal vocabulary service
                        get_action('vocabulary_service_term_upsert')(context, {
                            'vocabulary_service_id': service_id,
                            'label': label,
                            'uri': uri,
                        })
                return True

        except Exception as e:
            log.error('>>> ERROR attempting to fetch vocabulary from CKAN CSV')
            log.error(str(e))

    return False
