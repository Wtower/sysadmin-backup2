""" Test tar local """
import unittest
from unittest.mock import Mock, patch
import sys
import shutil
from core.app import Backup


class BasicBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_basic.conf.yml'
    destination = '/tmp/spufd2'

    def test_local(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertNotIn("DEBUG Mounted device", stderr)
        self.assertIn("DEBUG Not incremental backup", stderr)
        self.assertIn("DEBUG Elapsed time", stderr)
        stdout = sys.stdout.getvalue()
        self.assertIn('sysadmin-backup', stdout)
        self.assertIn("Performing backup", stdout)
        self.assertIn('Backup finished', stdout)

    class MockShTar(Mock):
        class ErrorReturnCode(BaseException):
            stderr = "Simulated error"

        def tar(self, *args, **kwargs):
            raise self.ErrorReturnCode

    mock_sh_tar = MockShTar()

    @patch('backup.tar.sh', new=mock_sh_tar)
    def test_exception(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn("CRITICAL Backup failure: %s" % self.mock_sh_tar.ErrorReturnCode.stderr, stderr)

    def tearDown(self):
        shutil.rmtree(self.destination, ignore_errors=True)
