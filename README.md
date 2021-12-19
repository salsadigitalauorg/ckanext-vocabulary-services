# ckanext-vocabulary-services

## Setup

Add the extension to your CKAN `.ini` file:

    ckan.plugins = ... vocabulary_services ...

Create the database tables:

    ckan -c path/to/ckan.ini vocabulary-services-init-db

This will create the following two tables:

    vocabulary_service
    vocabulary_service_term

Update the database tables:

    ckan db upgrade -p vocabulary_services

*(NOT to be confused with the CKAN core `vocabulary` table)*

## Background tasks

A cron job needs to be set up to refresh the vocabulary sevices periodically based on each `vocabulary_service.update_frequency` setting.

    ckan -c path/to/ckan.ini vocabulary-services-refresh

## Secure Vocabularies

A secure vocabulary is an ecnrypted CSV that is not stored in the `vocabulary_service` or `vocabulary_service_term`
database tables.

To enable secure vocabularies, enable the `secure_vocabularies` plugin in CKAN `.ini` file, e.g.
   
    ckan.plugins = ... secure_vocabularies ...
    
You must also specify a path to a secure vocabulary configuration file, i.e.

    ckan.vocabulary_services.configuration_file = /etc/ckan/default/secure_vocabularies.json

... to be continued ...

