""" Test tar local """
import unittest
import sys
import shutil
from core.app import Backup


class BasicBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_basic.conf.yml'

    def test_backup_local(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertNotIn("DEBUG Mounted device", stderr)
        self.assertIn("DEBUG Elapsed time", stderr)
        stdout = sys.stdout.getvalue()
        self.assertIn('sysadmin-backup', stdout)
        self.assertIn("Performing backup", stdout)
        self.assertIn('Backup finished', stdout)

    def tearDown(self):
        shutil.rmtree('/tmp/spufd2', ignore_errors=True)
