""" Mount filesystem """
import logging
import sh


# noinspection PyUnresolvedReferences,PyUnusedLocal
class Mount:
    def __init__(self, configuration):
        self.logger = logging.getLogger('backup.mount')
        self.configuration = configuration

    def __enter__(self):
        if self.configuration['type'] != 'usb':
            return self
        try:
            sh.mount(self.configuration['device'], self.configuration['destination'])
        except sh.ErrorReturnCode_32:
            self.logger.debug("Device already mounted")
        else:
            self.logger.debug("Mounted device")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:  # pragma: nocover
            self.logger.error('Mount exception %s: %s' % exc_type, exc_val)
            return False
        if self.configuration['type'] != 'usb':
            return self
        sh.umount('-l', '/dev/sdf')
        self.logger.debug("Unmounted device")
        return self
