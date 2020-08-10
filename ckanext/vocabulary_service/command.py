from ckan.lib.cli import CkanCommand


class InitDBCommand(CkanCommand):
    """
    Initialises the database with the required tables
    Connects to the CKAN database and creates the vocabulary services tables.
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0


    def __init__(self, name):
        super(InitDBCommand, self).__init__(name)

    def command(self):
        self._load_config()

        import logging
        import model

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
