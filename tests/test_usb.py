""" Test tar usb """
import unittest
from unittest.mock import Mock, patch, call
import sys
import os
import shutil
from core.app import Backup


class UsbBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_usb.conf.yml'
    destination = '/tmp/spufd2'
    device = '/dev/sdf'

    @patch('core.mount.sh')
    def test_external(self, mock_sh):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        # Let this test create destination to increase branch coverage
        if not os.path.exists(self.destination):
            os.makedirs(self.destination)
        Backup()
        self.assertIn(call.mount(self.device, self.destination), mock_sh.method_calls)
        self.assertIn(call.umount('-l', self.device), mock_sh.method_calls)
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertIn("DEBUG Mounted device", stderr)
        self.assertIn("DEBUG Unmounted device", stderr)

    class MockShMounted(Mock):
        # noinspection PyPep8Naming
        class ErrorReturnCode_32(BaseException):
            pass

        def mount(self, *args):
            raise self.ErrorReturnCode_32

    mock_sh_mounted = MockShMounted()

    @patch('core.mount.sh', new=mock_sh_mounted)
    def test_mounted(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn("DEBUG Device already mounted", stderr)
        self.assertIn("DEBUG Unmounted device", stderr)

    def tearDown(self):
        shutil.rmtree(self.destination, ignore_errors=True)
