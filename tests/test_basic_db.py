""" Test db dump """
import unittest
from unittest.mock import Mock, patch, call
import sys
import shutil
from core.app import Backup


class BasicDBBackupTestCase(unittest.TestCase):
    conf_file = 'tests/test_basic_db.conf.yml'

    @patch('backup.backup.sh')
    def test_db(self, mock_sh):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        self.assertIn(
            call.mysqldump('--defaults-extra-file=~/.my.cnf', '--all-databases', _out='/tmp/spufd2/mysqldump.sql'),
            mock_sh.method_calls)
        stderr = sys.stderr.getvalue()
        self.assertIn(self.conf_file, stderr)
        self.assertIn("DEBUG Performed mysql dump", stderr)

    @patch('backup.backup.sh')
    def test_dry_run(self, mock_sh):
        sys.argv = [sys.argv[0], '-n', '-vvvv', self.conf_file]
        Backup()
        self.assertIn(
            call.mysqldump('--defaults-extra-file=~/.my.cnf', '--all-databases', _out=None),
            mock_sh.method_calls)

    class MockShDump(Mock):
        class ErrorReturnCode(BaseException):
            stderr = "Simulated error"

        def mysqldump(self, *args, **kwargs):
            raise self.ErrorReturnCode

    mock_sh_dump = MockShDump()

    @patch('backup.backup.sh', new=mock_sh_dump)
    def test_unhandled(self):
        sys.argv = [sys.argv[0], '-vvvv', self.conf_file]
        Backup()
        stderr = sys.stderr.getvalue()
        self.assertIn("ERROR Unable to perform mysqldump: %s" % self.mock_sh_dump.ErrorReturnCode.stderr, stderr)

    def tearDown(self):
        shutil.rmtree('/tmp/spufd2', ignore_errors=True)
