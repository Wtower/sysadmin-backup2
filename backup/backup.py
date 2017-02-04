""" Abstract class for all backup methods """
import time
import logging
import os
import sh
from abc import ABCMeta, abstractmethod
from core.mount import Mount


# noinspection PyUnresolvedReferences
class BackupMethod:
    __metaclass__ = ABCMeta
    lock_file = '/tmp/sysadmin-backup'

    def __init__(self, configuration, arguments):
        self.start_time = time.time()
        self.configuration = configuration
        self.arguments = arguments
        self.mount = Mount(configuration['destination'])
        self.logger = logging.getLogger('backup')

    def stat(self):
        return time.time() - self.start_time

    def mysql_dump(self):
        if self.configuration['backup'].get('mysqldump', None):
            destination = None
            if not self.arguments.dry_run:
                destination = self.configuration['destination'].get(
                    'database',
                    self.configuration['destination']['destination'])
                destination = os.path.join(destination, 'mysqldump.sql')
            self.logger.debug('Mysqldump destination: %s', destination)
            try:
                sh.mysqldump('--defaults-extra-file=~/.my.cnf', '--all-databases', _out=destination)
            except sh.ErrorReturnCode as exc:
                self.logger.error("Unable to perform mysqldump: %s", exc.stderr)
            else:
                self.logger.debug("Performed mysql dump")

    @abstractmethod
    def execute(self):
        self.mysql_dump()
