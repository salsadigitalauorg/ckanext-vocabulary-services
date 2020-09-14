# -*- coding: utf-8 -*-

import click
import logging

from ckanapi import LocalCKAN, ValidationError
from ckanext.vocabulary_services import model
from datetime import datetime

log = logging.getLogger(__name__)


def refresh_required(service):
    utc_now = datetime.utcnow()

    # If a vocabulary_service does not have a `date_last_processed` refresh it
    # i.e. it has never been processed
    if not service.date_last_processed:
        return True

    delta = utc_now - service.date_last_processed

    log.debug('>>> UTC now: %s' % utc_now)
    log.debug('>>> Update frequency: %s' % service.update_frequency)
    log.debug('>>> Last processed: %s' % service.date_last_processed)
    log.debug('>>> Delta: %s' % delta)
    log.debug('>>> Delta (total seconds): %s' % delta.total_seconds())

    if service.update_frequency == 'daily':
        if delta.total_seconds() / (60 * 60 * 24) > 1:
            return True
        else:
            return False
    elif service.update_frequency == 'weekly':
        if delta.total_seconds() / (60 * 60 * 24 * 7) > 1:
            return True
        else:
            return False
    elif service.update_frequency == 'monthly':
        if delta.total_seconds() / (60 * 60 * 24 * 30) > 1:
            return True
        else:
            return False


@click.command(u"vocabulary-services-refresh")
def refresh_cmd():
    """Refresh each of the internal vocabulary services' terms (if required)
    """
    registry = LocalCKAN()

    try:
        # Load all vocabulary_service records
        vocabulary_services = model.VocabularyService.all()

        # Check each vocabulary_service to see if it needs to be refreshed
        for service in vocabulary_services:
            if refresh_required(service):
                click.secho(u"Needs updating", fg=u"yellow")
                registry.action.update_vocabulary_terms(id=service.id, uri=service.uri, type=service.type)
            else:
                click.secho(u"Doesn't need updating", fg=u"green")

    except ValidationError as e:
        log.error(str(e))

    click.secho(u"COMPLETED: vocabulary-services-refresh", fg=u"green")


@click.command(u"vocabulary-services-init-db")
def init_db_cmd():
    """Initialise the database tables required for internal vocabulary services
    """
    click.secho(u"Initializing vocabulary services tables", fg=u"green")

    try:
        model.vocabulary_service_table.create()
    except Exception as e:
        log.error(str(e))

    try:
        model.vocabulary_service_term_table.create()
    except Exception as e:
        log.error(str(e))

    click.secho(u"Vocabulary services tables are setup", fg=u"green")


def get_commands():
    return [init_db_cmd, refresh_cmd]
