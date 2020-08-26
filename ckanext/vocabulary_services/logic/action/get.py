import logging
import requests

from ckan.plugins.toolkit import get_action
from ckanext.vocabulary_services import model

log = logging.getLogger(__name__)


def vocabulary_services(context, data_dict):
    # @TODO: check access / write authentication function
    services = []

    try:
        services = model.VocabularyService.all()
    except Exception as e:
        log.error(str(e))

    return services


def vocabulary_service(context, reference):
    # @TODO: check access / write authentication function
    return model.VocabularyService.get(reference)


def vocabulary_service_terms(context, name):
    # @TODO: check access / write authentication function
    terms = []

    try:
        data = vocabulary_service(context, name)
        terms = data.terms
    except Exception as e:
        log.error(str(e))

    return terms


def csiro_vocabulary_terms(context, service):
    """
    Query the externally hosted vocabulary and extract the terms out into our internal
    vocabulary service.
    Example:
        http://registry.it.csiro.au/def/isotc211/MD_SpatialRepresentationTypeCode

    This example has multiple output types - for this example we will attempt to use
    the JSON-LD endpoint:

        http://registry.it.csiro.au/def/isotc211/MD_SpatialRepresentationTypeCode?_format=jsonld
    """
    try:
        r = requests.get(service.uri)
        log.debug(r.status_code)

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
                    get_action('vocabulary_service_term_create')({}, {
                        'vocabulary_service_id': service.id,
                        'label': label,
                        'uri': uri,
                    })
        return True

    except Exception as e:
        log.error(str(e))

    return False


def vocprez_vocabulary_terms(context, service):
    """
    Query the externally hosted vocabulary and extract the terms out into our internal
    vocabulary service.
    Example:
        https://vocabs.gsq.digital/endpoint?query=PREFIX%20skos%3A%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3ESELECT%3Fconcept%3FprefLabel%20WHERE%7B%3Fconcept%20a%20skos%3AConcept%3Bskos%3AprefLabel%3FprefLabel%3Bskos%3AinScheme%3Chttp%3A%2F%2Flinked.data.gov.au%2Fdef%2Fgsq-dataset-theme%3E.%7Dorder%20by%3FprefLabel&Accept=application/sparql-results+json
    """
    try:
        r = requests.get(service.uri)
        log.debug(r.status_code)

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
                    get_action('vocabulary_service_term_create')({}, {
                        'vocabulary_service_id': service.id,
                        'label': pref_label['value'],
                        'uri': concept['value'],
                    })
            return True

    except Exception as e:
        log.error(str(e))

    return False
