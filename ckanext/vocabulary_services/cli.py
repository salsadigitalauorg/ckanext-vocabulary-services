# -*- coding: utf-8 -*-

import ckan.plugins.toolkit as toolkit
import click
import logging
import os

from ckan.views.admin import _get_sysadmins
from ckanapi import LocalCKAN, ValidationError
from ckanext.invalid_uris.helpers import valid_uri
from ckanext.vocabulary_services import model
import datetime

log = logging.getLogger(__name__)
config = toolkit.config


def refresh_required(service):
    utc_now = datetime.datetime.now(datetime.timezone.utc)

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
    elif service.update_frequency == 'never':
        return False


@click.command(u"vocabulary-services-refresh")
@click.pass_context
def refresh_cmd(ctx):
    """Refresh each of the internal vocabulary services' terms (if required)
    """
    registry = LocalCKAN()

    try:
        # Load all vocabulary_service records
        vocabulary_services = model.VocabularyService.all()

        # Validate uri.
        invalid_services = []
        for service in vocabulary_services:
            valid_uri_resp = valid_uri(service.uri)
            if not valid_uri_resp.get('valid'):
                invalid_services.append(service)

        if invalid_services and not os.environ.get('DISABLE_CRON_JOB_EMAILS'):
            admins = _get_sysadmins().all()
            for admin in admins:
                if admin.email:
                    try:
                        flask_app = ctx.meta['flask_app']
                        with flask_app.test_request_context():
                            subject = 'QESD catalogue – vocabulary service update error'
                            body = toolkit.render(
                                'emails/body/vocab_service_invalid_urls.txt',
                                {
                                    'invalid_services': invalid_services,
                                    'current_utc': datetime.datetime.now(datetime.timezone.utc)
                                }
                            )
                            body_html = toolkit.render(
                                'emails/body/vocab_service_invalid_urls.html',
                                {
                                    'invalid_services': invalid_services,
                                    'current_utc': datetime.datetime.now(datetime.timezone.utc)
                                }
                            )
                            # Improvements for job worker visibility when troubleshooting via logs
                            job_title = f'Vocabulary service update error: Sending email to {admin.name}'
                            toolkit.enqueue_job(toolkit.mail_recipient, [admin.name, admin.email, subject, body, body_html], title=job_title)
                    except Exception as e:
                        log.error(e)
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


def get_commands():
    return [refresh_cmd]
