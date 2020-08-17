# ckanext-vocabulary-services

## Setup

Add the extension to your CKAN `.ini` file:

    ckan.plugins = ... vocabulary_services ...

Create the database tables:

    ckan -c path/to/ckan.ini vocabulary-services-init-db

This will create the following two tables:

    vocabulary_service
    vocabulary_service_term

*(NOT to be confused with the CKAN core `vocabulary` table)*
