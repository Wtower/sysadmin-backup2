""" Mount filesystem """
import logging
import os
import sh


# noinspection PyUnresolvedReferences,PyUnusedLocal
class Mount:
    def __init__(self, configuration):
        self.logger = logging.getLogger('backup.mount')
        self.configuration = configuration
        self.crypt_is_open = False
        self.is_mounted = False

    def __enter__(self):
        self.check_destination()
        if self.configuration['type'] != 'usb':
            return self
        self.crypt_open()
        self.mount()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:  # pragma: nocover
            self.logger.error("Unhandled exception %s: %s", exc_type, exc_val)
            return False
        self.unmount()
        self.crypt_close()
        return self

    def check_destination(self):
        if not os.path.exists(self.configuration['destination']):
            os.makedirs(self.configuration['destination'])
            self.logger.debug("Created destination directory")

    def mount(self):
        try:
            sh.mount(self.configuration['device'], self.configuration['destination'])
        except sh.ErrorReturnCode_32:
            self.logger.debug("Device already mounted")
        else:
            self.logger.debug("Mounted device")
        self.is_mounted = True

    def unmount(self):
        if self.is_mounted:
            sh.umount('-l', self.configuration['destination'])
            self.logger.debug("Unmounted device")
            self.is_mounted = False

    def crypt_open(self):
        if self.configuration.get('encrypted_key', None):
            sh.cryptsetup(
                'luksOpen',
                '-d', self.configuration['encrypted_key'],
                self.configuration['device'],
                self.configuration['encrypted_map'])
            self.logger.debug("Opened encrypted device")
            self.crypt_is_open = True
            self.configuration['crypt_device'] = self.configuration['device']
            self.configuration['device'] = os.path.join('/dev', 'mapper', self.configuration['encrypted_map'])

    def crypt_close(self):
        if self.crypt_is_open:
            sh.cryptsetup('luksClose', self.configuration['encrypted_map'])
            self.logger.debug("Closed encrypted device")
            self.crypt_is_open = False
            self.configuration['device'] = self.configuration['crypt_device']
