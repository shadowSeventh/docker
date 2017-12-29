# -*- coding: utf8 -*-

import unittest
from certbot_adc.CadcUtils import CadcUtils


class TestCadcUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_split_domain_name_00(self):
        try:
            result = CadcUtils.split_domain_name(None)
            self.assertTrue(False, "should not run to here")
        except AssertionError as e:
            self.assertTrue(e)

    def test_split_domain_name_01(self):
        result = CadcUtils.split_domain_name("kingsilk.net")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "")
        self.assertEqual(result[0][1], "kingsilk.net")

    def test_split_domain_name_02(self):
        result = CadcUtils.split_domain_name("aaa.test13.kingsilk.com.cn")
        self.assertEqual(len(result), 4)

        self.assertEqual(result[0][0], "aaa.test13.kingsilk")
        self.assertEqual(result[0][1], "com.cn")

        self.assertEqual(result[1][0], "aaa.test13")
        self.assertEqual(result[1][1], "kingsilk.com.cn")

        self.assertEqual(result[2][0], "aaa")
        self.assertEqual(result[2][1], "test13.kingsilk.com.cn")

        self.assertEqual(result[3][0], "")
        self.assertEqual(result[3][1], "aaa.test13.kingsilk.com.cn")


if __name__ == '__main__':
    unittest.main()
