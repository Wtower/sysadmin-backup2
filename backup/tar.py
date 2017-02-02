""" Tar backup method """
import logging
import fasteners
from backup import BackupMethod


class Tar(BackupMethod):
    @fasteners.interprocess_locked(BackupMethod.lock_file)
    def execute(self):
        logger = logging.getLogger('backup.tar')
        with self.mount:
            print('exec')
        logger.debug('Elapsed time: %.3f sec' % self.stat())
