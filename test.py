import unittest
from tests.test_basic import BasicBackupTestCase
from tests.test_basic_inc import BasicIncBackupTestCase
from tests.test_basic_inc_full import BasicIncFullBackupTestCase
from tests.test_basic_db import BasicDBBackupTestCase
from tests.test_usb import UsbBackupTestCase
from tests.test_usb_enc import UsbEncBackupTestCase


if __name__ == '__main__':
    unittest.main(buffer=True)
