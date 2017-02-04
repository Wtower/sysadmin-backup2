""" Unit tests """
import unittest
from unittest.mock import patch, call
import sys
import os
import shutil
from core.app import Backup


class UsbEncBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_usb_enc.conf.yml'

    @patch('core.mount.sh')
    def test_backup_external_encrypted(self, mock_sh):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        # Let this test create destination to increase branch coverage
        os.makedirs('/tmp/spufd2')
        Backup()
        self.assertIn(
            call.cryptsetup('luksOpen', '-d', '/root/backup-external-key', '/dev/sdf', 'backup-external'),
            mock_sh.method_calls)
        self.assertIn(call.mount('/dev/sdf', '/tmp/spufd2'), mock_sh.method_calls)
        self.assertIn(call.umount('-l', '/dev/sdf'), mock_sh.method_calls)
        self.assertIn(call.cryptsetup('luksClose', 'backup-external'), mock_sh.method_calls)
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertIn("DEBUG Opened encrypted device", stderr)
        self.assertIn("DEBUG Closed encrypted device", stderr)

    def tearDown(self):
        shutil.rmtree('/tmp/spufd2')
