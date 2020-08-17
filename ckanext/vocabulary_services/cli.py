# -*- coding: utf-8 -*-

import click
import ckan.plugins.toolkit as tk


@click.command(u"example-iclick-hello")
def hello_cmd():
    """Example of single command.
    """
    click.secho(u"Hello, World!", fg=u"green")


@click.command(u"vocabulary-services-init-db")
def init_db_cmd():
    """Example of single command.
    """
    click.secho(u"Hello init, World!", fg=u"green")

    import logging
    from ckanext.vocabulary_services import model

    log = logging.getLogger(__name__)

    log.info("starting command")

    log.info("Initializing vocabulary services tables")

    try:
        model.vocabulary_service_table.create()
    except Exception as e:
        log.error(str(e))

    try:
        model.vocabulary_service_term_table.create()
    except Exception as e:
        log.error(str(e))

    log.info("Vocabulary services tables are setup")

@click.group(u"example-iclick-bye")
def bye_cmd():
    """Example of group of commands.
    """
    pass


@bye_cmd.command()
@click.argument(u"name", required=False)
def bye(name):
    """Command with optional argument.
    """
    if not name:
        tk.error_shout(u"I do not know your name.")
    else:
        click.secho(u"Bye, {}".format(name))


def get_commands():
    return [hello_cmd, bye_cmd, init_db_cmd]
