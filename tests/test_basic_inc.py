""" Test tar local incremental """
import unittest
import sys
import os
import shutil
from datetime import datetime
from core.app import Backup


class BasicIncBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_basic_inc.conf.yml'
    destination = '/tmp/spufd2'
    frequency = '%Y-%m-%d'

    def test_inc(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertNotIn("DEBUG Mounted device", stderr)
        self.assertNotIn("DEBUG Not incremental backup", stderr)
        self.assertIn("DEBUG Snar file not exists", stderr)
        self.assertIn('cpzfv', stderr)
        self.assertIn("DEBUG Elapsed time", stderr)
        stdout = sys.stdout.getvalue()
        self.assertIn('sysadmin-backup', stdout)
        self.assertIn("Performing backup", stdout)
        self.assertIn('Backup finished', stdout)
        date_stamp = datetime.now().strftime(self.frequency)
        bak = os.path.join(self.destination, 'test_basic_inc.%s.tar.gz' % date_stamp)
        self.assertTrue(os.path.exists(bak))

    def test_snar_exists(self):
        os.makedirs(self.destination, exist_ok=True)
        snar = os.path.join(self.destination, 'test_basic_inc.snar')
        open(snar, 'w').close()
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertNotIn("DEBUG Snar file not exists", stderr)
        self.assertIn("DEBUG Full backup frequency not defined", stderr)
        os.remove(snar)

    def test_backup_exists(self):
        os.makedirs(self.destination, exist_ok=True)
        date_stamp = datetime.now().strftime(self.frequency)
        bak = os.path.join(self.destination, 'test_basic_inc.%s.tar.gz' % date_stamp)
        open(bak, 'w').close()
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn("DEBUG Backup file test_basic_inc.%s already exists" % date_stamp, stderr)
        os.remove(bak)

    def test_no_verbosity(self):
        sys.argv = [sys.argv[0], self.conf_file]
        Backup()
        stdout = sys.stdout.getvalue()
        self.assertIn('Backup finished', stdout)

    def tearDown(self):
        shutil.rmtree(self.destination, ignore_errors=True)
