import sys
import unittest
from ..btsport_login import BtSportLogin


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.username = ''  # todo: get from xbmc config
        self.password = ''

    def test_login(self):
        BtSportLogin(self.username, self.password)

if __name__ == '__main__':
    unittest.main()
