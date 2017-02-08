""" Test tar local """
import unittest
from unittest.mock import Mock, patch
import sys
import shutil
from core.app import Backup


class RSyncBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_rsync.conf.yml'
    destination = '/tmp/spufd2'

    def test_rsync(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertNotIn("DEBUG Mounted device", stderr)
        self.assertIn("DEBUG Not incremental backup", stderr)
        self.assertNotIn("DEBUG Ignoring existing files", stderr)
        self.assertIn("DEBUG Elapsed time", stderr)
        stdout = sys.stdout.getvalue()
        self.assertIn('sysadmin-backup', stdout)
        self.assertIn("Performing backup", stdout)
        self.assertIn('Backup finished', stdout)

    def test_no_verbosity(self):
        sys.argv = [sys.argv[0], self.conf_file]
        Backup()
        stdout = sys.stdout.getvalue()
        self.assertIn('Backup finished', stdout)

    def test_dry_run(self):
        sys.argv = [sys.argv[0], '-vvvv', '-n', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn("-n", stderr)

    class MockShRsync(Mock):
        class ErrorReturnCode(BaseException):
            stderr = "Simulated error"

        def rsync(self, *args, **kwargs):
            raise self.ErrorReturnCode

    mock_sh_rsync = MockShRsync()

    @patch('backup.rsync.sh', new=mock_sh_rsync)
    def test_exception(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn("CRITICAL Backup failure: %s" % self.mock_sh_rsync.ErrorReturnCode.stderr, stderr)

    def tearDown(self):
        shutil.rmtree(self.destination, ignore_errors=True)
