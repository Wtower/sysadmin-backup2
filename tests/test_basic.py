""" Unit tests """
import unittest
import sys
import shutil
from core.app import Backup


class BasicBackupTestCase(unittest.TestCase):
    def test_backup_local(self):
        sys.argv = [sys.argv[0], '-vvvv', 'tests/test_basic.conf.yml']
        Backup()
        stderr = sys.stderr.getvalue()
        # self.assertIn('conf/sample_local.conf.yml', stderr)
        self.assertNotIn("DEBUG Mounted device", stderr)

    def tearDown(self):
        shutil.rmtree('/tmp/spufd2')
