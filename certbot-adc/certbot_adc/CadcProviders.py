# -*- coding: utf8 -*-

from aliyunsdkcore.client import AcsClient
from QcloudApi.qcloudapi import QcloudApi

from CadcConf import CadcConf
from CadcProviderBase import CadcProviderBase
from CadcProviderAliyun import CadcProviderAliyun
from CadcProviderQcloud import CadcProviderQcloud


class CadcProviders(CadcProviderBase):
    cadc_conf = None

    def __init__(self, cadc_conf_file=None):
        self.cadc_conf = CadcConf(cadc_conf_file)

    def get_dns_provider(self, domain):

        dns_provider = self.cadc_conf.find_provider_by_domain(domain)

        assert dns_provider, "'" + domain + "' is not configured."

        t = dns_provider.get("type")

        if t == "aliyun":
            acs_client = AcsClient(
                dns_provider.get("keyId"),
                dns_provider.get("keySecret"),
                dns_provider.get("region")
            )
            return CadcProviderAliyun(acs_client)
        elif t == "qcloud":
            api = QcloudApi("cns", {
                'Region': dns_provider["region"],
                'secretId': dns_provider["keyId"],
                'secretKey': dns_provider["keySecret"],
                'method': 'get'
            })
            return CadcProviderQcloud(api)

        else:
            assert False, "Not supported provider type '" + t + "'"

    def update_dns01(self, domain, token):
        dns_provider = self.get_dns_provider(domain)
        dns_provider.update_dns01(domain, token)

    def clean_dns01(self, domain):
        dns_provider = self.get_dns_provider(domain)
        dns_provider.clean_dns01(domain)
