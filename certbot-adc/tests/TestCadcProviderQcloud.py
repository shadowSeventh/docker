# -*- coding: utf8 -*-

import unittest

from QcloudApi.qcloudapi import QcloudApi

from certbot_adc.CadcUtils import CadcUtils
from certbot_adc.CadcConf import CadcConf
from certbot_adc.CadcProviderQcloud import CadcProviderQcloud


class TestCadcProviderQcloud(unittest.TestCase):
    api = None
    q = None

    def setUp(self):
        cadc_conf = CadcConf("../.tmp/certbot_adc.yaml")

        p = cadc_conf.name_mappings.get("btpka3")

        self.api = QcloudApi("cns", {
            'Region': p["region"],
            'secretId': p["keyId"],
            'secretKey': p["keySecret"],
            'method': 'get'
        })
        self.q = CadcProviderQcloud(self.api)

    def tearDown(self):
        pass

    # ---------------------------------- qc test
    def test_qc_DomainList(self):
        resp = self.api.call("DomainList", {
            "offset": 0,
            "length": 100
        })
        print(resp)

    def test_qc_RecordList(self):
        resp = self.api.call("RecordList", {
            "domain": "btpka3.xyz",
            "offset": 0,
            "length": 100,
            "recordType": "TXT"
        })
        print(resp)

    def test_qc_RecordModify(self):
        resp = self.api.call("RecordModify", {
            "domain": "btpka3.xyz",
            "recordId": 329336901,
            "subDomain": "dd",
            "recordType": "TXT",
            "recordLine": "默认",
            "value": "999"

        })
        print(resp)

    def test_qc_RecordCreate(self):
        resp = self.api.call("RecordCreate", {
            "domain": "btpka3.xyz",
            "subDomain": "ee",
            "recordType": "TXT",
            "recordLine": "默认",
            "value": "888"

        })
        print(resp)

    def test_qc_RecordDelete(self, ):
        resp = self.api.call("RecordDelete", {
            "domain": "btpka3.xyz",
            "recordId": 329594478
        })
        print(resp)

    # ---------------------------------- CadcProviderQcloud test


    def test_get_txt_record_1(self):
        self.assertTrue(self.q.get_txt_record("dd", "btpka3.xyz"))
        self.assertFalse(self.q.get_txt_record("ss", "btpka3.xyz"))

    def test_owns_domain_1(self):
        result = self.q.owns_domain("btpka3.xyz")

        self.assertTrue(result is not None)
        self.assertTrue(type(result) == tuple)
        self.assertTrue(len(result) == 2)
        self.assertTrue(result[0] == "")
        self.assertTrue(result[1] == "btpka3.xyz")

    def test_owns_domain_2(self):
        result = self.q.owns_domain("btpka3.com")

        self.assertTrue(result is None)

    def test_update_dns01_1(self):
        self.q.update_dns01("btpka3.xyz", "8888")


if __name__ == '__main__':
    unittest.main()
