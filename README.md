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

## Background tasks

A cron job needs to be set up to refresh the vocabulary sevices periodically based on each `vocabulary_service.update_frequency` setting.

    ckan -c path/to/ckan.ini vocabulary-services-refresh

