""" Test tar usb encrypted """
import unittest
from unittest.mock import Mock, patch, call
import sys
import shutil
from core.app import Backup


class UsbEncBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_usb_enc.conf.yml'
    destination = '/tmp/spufd2'
    device = '/dev/sdf'
    encrypted_map = 'backup-external'

    @patch('core.mount.sh')
    def test_external_encrypted(self, mock_sh):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        self.assertIn(
            call.cryptsetup('luksOpen', '-d', '/root/backup-external-key', self.device, self.encrypted_map),
            mock_sh.method_calls)
        self.assertIn(call.mount('/dev/mapper/%s' % self.encrypted_map, self.destination), mock_sh.method_calls)
        self.assertIn(call.umount('-l', self.destination), mock_sh.method_calls)
        self.assertIn(call.cryptsetup('luksClose', self.encrypted_map), mock_sh.method_calls)
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertIn("DEBUG Opened encrypted device", stderr)
        self.assertIn("DEBUG Closed encrypted device", stderr)

    class MockShDevUnavailable(Mock):
        # noinspection PyPep8Naming
        class ErrorReturnCode_4(BaseException):
            pass

        def cryptsetup(self, *args):
            raise self.ErrorReturnCode_4

    mock_sh_dev_unavailable = MockShDevUnavailable()

    @patch('core.mount.sh', new=mock_sh_dev_unavailable)
    def test_dev_unavailable(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        with self.assertRaises(SystemExit):
            Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn("DEBUG Device unavailable", stderr)

    def tearDown(self):
        shutil.rmtree(self.destination, ignore_errors=True)
