""" Rsync backup method """
import logging
import fasteners
import os
import sh
from backup import BackupMethod


class RSync(BackupMethod):
    @fasteners.interprocess_locked(BackupMethod.lock_file)
    def execute(self):
        logger = logging.getLogger('backup.rsync')
        with self.mount:
            print("Performing backup")
            logger.debug("Initiating backup")
            super(RSync, self).execute()

            if self.configuration['backup'].get('incremental', False):
                rsync_args = [
                    '-abs', '--no-links', '--delete',
                    '--backup-dir=%s' % os.path.join(
                        self.configuration['destination']['incremental_destination'], self.date_stamp)]
            else:
                logger.debug("Not incremental backup")
                rsync_args = ['-as', '--no-links']
                if self.configuration['backup'].get('ignore_existing', False):
                    logger.debug("Ignoring existing files")
                    rsync_args.append('--delete')

            if self.arguments.verbosity:
                rsync_args.append('-v')
            if self.arguments.dry_run:
                rsync_args.append('-n')
            if self.configuration['destination']['type'] == 'ssh':
                rsync_args.extend(('-e', 'ssh'))
            for exclude in self.configuration['backup'].get('excludes', []):
                rsync_args.append('--exclude=%s' % exclude)
            rsync_args.append(self.configuration['backup']['directories'][0] + '/')
            rsync_args.append(self.configuration['destination']['destination'])

            logger.debug(rsync_args)
            try:
                # noinspection PyUnresolvedReferences
                sh.rsync(*rsync_args)
            except sh.ErrorReturnCode as exc:
                logger.critical("Backup failure: %s", exc.stderr)
            else:
                print("Backup finished")
                logger.info("Backup successfully completed.")
                logger.debug("Elapsed time: %.3f sec", self.stat())
