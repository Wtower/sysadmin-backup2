""" Unit tests """
import unittest
from unittest.mock import Mock, patch, call
import sys
from core.app import Backup


class BackupTestCase(unittest.TestCase):
    @patch('core.mount.sh')
    def test_backup_external(self, mock_sh):
        sys.argv = [sys.argv[0], '-vvvv', 'conf/sample_external.conf.yml']
        Backup()
        self.assertIn(call.mount('/dev/sdf', '/tmp/spufd2'), mock_sh.method_calls)
        self.assertIn(call.umount('-l', '/dev/sdf'), mock_sh.method_calls)
        stderr = sys.stderr.getvalue()
        self.assertIn('conf/sample_external.conf.yml', stderr)
        self.assertIn('DEBUG Mounted device', stderr)
        self.assertIn('DEBUG Unmounted device', stderr)
        stdout = sys.stderr.getvalue()
        self.assertIn('sysadmin-backup', stdout)

    class MockShMounted(Mock):
        # noinspection PyPep8Naming
        class ErrorReturnCode_32(BaseException):
            pass

        def mount(self, *args):
            raise self.ErrorReturnCode_32

    mock_sh_mounted = MockShMounted()

    @patch('core.mount.sh', new=mock_sh_mounted)
    def test_backup_external_mounted(self):
        sys.argv = [sys.argv[0], '-vvvv', 'conf/sample_external.conf.yml']
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn('conf/sample_external.conf.yml', stderr)
        self.assertIn('DEBUG Device already mounted', stderr)
        self.assertIn('DEBUG Unmounted device', stderr)

    @patch('core.mount.sh')
    def test_backup_external_encrypted(self, mock_sh):
        sys.argv = [sys.argv[0], '-vvvv', 'conf/sample_external_enc.conf.yml']
        Backup()
        self.assertIn(
            call.cryptsetup('luksOpen', '-d', '/root/backup-external-key', '/dev/sdf', 'backup-external'),
            mock_sh.method_calls)
        self.assertIn(call.mount('/dev/sdf', '/tmp/spufd2'), mock_sh.method_calls)
        self.assertIn(call.umount('-l', '/dev/sdf'), mock_sh.method_calls)
        self.assertIn(call.cryptsetup('luksClose', 'backup-external'), mock_sh.method_calls)
        stderr = sys.stderr.getvalue()
        self.assertIn('conf/sample_external_enc.conf.yml', stderr)
        self.assertIn('DEBUG Opened encrypted device', stderr)
        self.assertIn('DEBUG Closed encrypted device', stderr)

    def test_backup_local(self):
        sys.argv = [sys.argv[0], '-vvvv', 'conf/sample_local.conf.yml']
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn('conf/sample_local.conf.yml', stderr)
        self.assertNotIn('DEBUG Mounted device', stderr)
