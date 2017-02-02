""" Main application """
import logging
import logging.config
import argparse
from ruamel import yaml
from backup import RSync, Tar

__version__ = 'v2.0.0'


class Backup:
    logging_handler_console_level_default = logging.CRITICAL

    def __init__(self):
        parser = argparse.ArgumentParser(description='sysadmin-backup')
        parser.add_argument('conf_file', type=open, help="Configuration file")
        parser.add_argument('-v', action='count', default=0, dest='verbosity', help="Verbosity level")
        parser.add_argument('--version', action='version', version=parser.description + ' ' + __version__)
        arguments = parser.parse_args()

        self.configuration = yaml.load(arguments.conf_file.read(), yaml.RoundTripLoader)
        self.logging_handler_console_level_default -= arguments.verbosity * 10
        self.configuration['logging']['handlers']['console']['level'] = self.logging_handler_console_level_default
        logging.config.dictConfig(self.configuration['logging'])
        logger = logging.getLogger('backup')

        print(parser.description)
        logger.debug(arguments)
        logger.debug(self.configuration['backup'])

        methods = {
            'rsync': RSync,
            'tar': Tar
        }
        backup = methods[self.configuration['backup']['type']]()
        backup.execute()
