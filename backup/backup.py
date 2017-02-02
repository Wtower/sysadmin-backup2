""" Abstract class for all backup methods """
from abc import ABCMeta, abstractmethod


class BackupMethod:
    __metaclass__ = ABCMeta
    lock_file = '/tmp/sysadmin-backup'

    def __init__(self):
        print('chk init')

    @abstractmethod
    def execute(self):
        pass  # pragma: nocover
