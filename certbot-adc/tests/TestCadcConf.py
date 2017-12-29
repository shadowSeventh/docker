# -*- coding: utf8 -*-

import unittest
from certbot_adc.CadcConf import CadcConf


class TestCadcConf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        CadcConf("../.tmp/certbot_adc.yaml")


if __name__ == '__main__':
    unittest.main()
