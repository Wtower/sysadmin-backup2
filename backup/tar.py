""" Tar backup method """
import fasteners
from backup import BackupMethod


class Tar(BackupMethod):
    @fasteners.interprocess_locked(BackupMethod.lock_file)
    def execute(self):
        print('exec')
