""" Test tar local incremental """
import unittest
import sys
import os
import shutil
from core.app import Backup


class BasicIncFullBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_basic_inc_full.conf.yml'
    destination = '/tmp/spufd2'

    def test_snar_exists(self):
        os.makedirs(self.destination, exist_ok=True)
        snar = os.path.join(self.destination, 'test_basic_inc_full.snar')
        open(snar, 'w').close()
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertNotIn("DEBUG Mounted device", stderr)
        self.assertNotIn("DEBUG Not incremental backup", stderr)
        self.assertNotIn("DEBUG Snar file not exists", stderr)
        self.assertNotIn("DEBUG Full backup frequency not defined", stderr)
        self.assertIn("DEBUG Snar file exists in current full backup period", stderr)
        self.assertIn("DEBUG Elapsed time", stderr)
        stdout = sys.stdout.getvalue()
        self.assertIn('sysadmin-backup', stdout)
        self.assertIn("Performing backup", stdout)
        self.assertIn('Backup finished', stdout)
        os.remove(snar)

    def test_snar_exists_outdated(self):
        os.makedirs(self.destination, exist_ok=True)
        snar = os.path.join(self.destination, 'test_basic_inc_full.snar')
        open(snar, 'w').close()
        os.utime(snar, (1, 1))  # set a very old time
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertNotIn("DEBUG Snar file exists in current full backup period", stderr)
        self.assertIn("DEBUG Removed outdated snar file", stderr)
        os.remove(snar)

    def tearDown(self):
        shutil.rmtree(self.destination, ignore_errors=True)
