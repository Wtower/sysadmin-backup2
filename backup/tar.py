""" Tar backup method """
import logging
import fasteners
import os
from datetime import datetime
import sh
from backup import BackupMethod


class Tar(BackupMethod):
    def snar_file_status(self, path_filename):
        """
        Check that a snar file exists in the current full backup frequency
        If exists but out of frequency then deletes it
        :param path_filename: the snar path file name
        :return: True if snar file exists and it is an incremental backup
        """
        logger = logging.getLogger('backup.tar.snar')
        if not self.configuration['backup'].get('incremental', False):
            logger.debug("Not incremental backup")
            return False
        if not os.path.exists(path_filename):
            logger.debug("Snar file not exists")
            return False
        if 'full_backup_frequency' not in self.configuration['backup']:
            logger.debug("Full backup frequency not defined")
            return True
        date_format = self.frequencies[self.configuration['backup']['full_backup_frequency']]
        if os.path.getmtime(path_filename).strftime(date_format) == datetime.now().strftime(date_format):
            logger.debug("Snar file exists in current full backup period")
            return True
        os.remove(path_filename)
        logger.debug("Removed outdated snar file")
        return False

    @fasteners.interprocess_locked(BackupMethod.lock_file)
    def execute(self):
        logger = logging.getLogger('backup.tar')
        with self.mount:
            date_stamp = datetime.now().strftime(self.frequencies[self.configuration['backup']['frequency']])
            filename = '%s.%s' % (self.conf_file_name, date_stamp)
            path_filename = os.path.join(self.configuration['destination']['destination'], filename)
            ext = '.tar.gz'

            if os.path.exists('%s%s' % (path_filename, ext)) or os.path.exists('%s.inc%s' % (path_filename, ext)):
                print("Backup already performed")
                logger.debug("Backup file %s already exists", path_filename)
                return

            print("Performing backup")
            logger.debug("Initiating backup")
            super(Tar, self).execute()

            tar_args = ['cpzf']
            if self.arguments.verbosity:
                tar_args[0] += 'v'

            partial = datetime.now().strftime('.partial-%H-%M-%S')
            snar_filename = '%s.snar' % self.conf_file_name
            snar_path_filename = os.path.join(self.configuration['destination']['destination'], snar_filename)
            if self.snar_file_status(snar_path_filename):
                ext = '.inc' + ext
            tar_args.append(path_filename + partial + ext)

            if self.configuration['backup'].get('incremental', False):
                tar_args.extend(('-g', snar_path_filename))
            for exclude in self.configuration['backup'].get('excludes', []):
                tar_args.append('--exclude=%s' % exclude)
            tar_args.extend(self.configuration['backup']['directories'])

            logger.debug(tar_args)
            if not self.arguments.dry_run:
                # noinspection PyUnresolvedReferences
                sh.tar(*tar_args)
                logger.debug("Files added to tar archive")
                os.rename(path_filename + partial + ext, path_filename + ext)

        print("Backup finished")
        logger.info("Backup successfully completed.")
        logger.debug("Elapsed time: %.3f sec", self.stat())
