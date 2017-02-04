""" Test db dump """
import unittest
from unittest.mock import Mock, patch, call
import sys
import shutil
from core.app import Backup


class BasicDBBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_basic_db.conf.yml'

    @patch('backup.backup.sh')
    def test_backup_db(self, mock_sh):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        self.assertIn(
            call.mysqldump('--defaults-extra-file=~/.my.cnf', '--all-databases', _out='/tmp/spufd2/mysqldump.sql'),
            mock_sh.method_calls)
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertIn("DEBUG Performed mysql dump", stderr)

    def tearDown(self):
        shutil.rmtree('/tmp/spufd2', ignore_errors=True)
