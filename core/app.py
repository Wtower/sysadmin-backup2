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
        parser.add_argument('-n', '--dry-run', action='store_true', help="Simulate backup")
        parser.add_argument('-v', action='count', default=0, dest='verbosity', help="Verbosity level")
        parser.add_argument('--version', action='version', version=parser.description + ' ' + __version__)
        arguments = parser.parse_args()

        configuration = yaml.load(arguments.conf_file.read(), yaml.RoundTripLoader)
        self.logging_handler_console_level_default -= arguments.verbosity * 10
        configuration['logging']['handlers']['console']['level'] = self.logging_handler_console_level_default
        logging.config.dictConfig(configuration['logging'])
        logger = logging.getLogger('backup')
        print(parser.description)
        logger.debug(arguments)

        methods = {
            'rsync': RSync,
            'tar': Tar
        }
        backup = methods[configuration['backup']['type']]
        backup(configuration, arguments).execute()
