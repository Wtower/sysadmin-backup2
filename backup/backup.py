""" Abstract class for all backup methods """
import time
from abc import ABCMeta, abstractmethod
from core.mount import Mount


class BackupMethod:
    __metaclass__ = ABCMeta
    lock_file = '/tmp/sysadmin-backup'

    def __init__(self, configuration):
        self.start_time = time.time()
        self.configuration = configuration
        self.mount = Mount(configuration['destination'])

    def stat(self):
        return time.time() - self.start_time

    @abstractmethod
    def execute(self):
        pass  # pragma: nocover
