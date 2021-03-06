""" Test tar local """
import unittest
import sys
import shutil
from core.app import Backup


class RSyncDelBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_rsync_delete.conf.yml'
    destination = '/tmp/spufd2'

    def test_rsync_delete_ssh(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertNotIn("DEBUG Mounted device", stderr)
        self.assertIn("DEBUG Not incremental backup", stderr)
        self.assertIn("DEBUG Ignoring existing files", stderr)
        self.assertIn("ssh", stderr)
        self.assertIn("DEBUG Elapsed time", stderr)
        stdout = sys.stdout.getvalue()
        self.assertIn('sysadmin-backup', stdout)
        self.assertIn("Performing backup", stdout)
        self.assertIn('Backup finished', stdout)

    def tearDown(self):
        shutil.rmtree(self.destination, ignore_errors=True)
