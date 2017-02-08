""" Abstract class for all backup methods """
import time
import logging
import os
import sh
from abc import ABCMeta, abstractmethod
from datetime import datetime
from core.mount import Mount


# noinspection PyUnresolvedReferences,PyUnusedLocal
class BackupMethod:
    __metaclass__ = ABCMeta
    lock_file = '/tmp/sysadmin-backup'
    frequencies = {
        'daily': '%Y-%m-%d',
        'weekly': '%Y-W%W',
        'monthly': '%Y-%m',
        'yearly': '%Y'
    }

    def __init__(self, configuration, arguments):
        self.start_time = time.time()
        self.configuration = configuration
        self.arguments = arguments
        self.mount = Mount(configuration['destination'])
        # Default values
        self.conf_file_name = os.path.basename(self.arguments.conf_file.name).split('.')[0]
        self.date_stamp = datetime.now().strftime(self.frequencies[self.configuration['backup']['frequency']])
        self.configuration['destination']['database'] = self.configuration['destination'].get(
            'database', self.configuration['destination']['destination'])

    def stat(self):
        return time.time() - self.start_time

    def mysql_dump(self):
        if self.configuration['backup'].get('mysqldump', None):
            logger = logging.getLogger('backup.mysqldump')
            destination = os.path.join(self.configuration['destination']['database'], 'mysqldump.sql')
            if self.arguments.dry_run:
                destination = None
            try:
                sh.mysqldump('--defaults-extra-file=~/.my.cnf', '--all-databases', _out=destination)
            except sh.ErrorReturnCode as exc:
                logger.error("Unable to perform mysqldump: %s", exc.stderr)
            else:
                logger.debug("Performed mysql dump")

    def postgres_dump(self):
        if self.configuration['backup'].get('postgresdump', None):
            logger = logging.getLogger('backup.postgresdump')
            destination = os.path.join(self.configuration['destination']['database'], 'postgresdump.sql')
            if self.arguments.dry_run:
                destination = None
            try:
                sh.pg_dumpall(_out=destination)
            except sh.ErrorReturnCode as exc:
                logger.error("Unable to perform postgresdump: %s", exc.stderr)
            else:
                logger.debug("Performed postgres dump")

    @abstractmethod
    def execute(self):
        self.mysql_dump()
        self.postgres_dump()
