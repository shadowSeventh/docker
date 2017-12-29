# -*- coding: utf8 -*-

from certbot_adc import CadcProviderBase, CadcConf


class CadcProviders(CadcProviderBase):
    cadc_conf: CadcConf

    def get_dns_provider(self, domain: str) -> CadcProviderBase: ...

    def update_dns01(self, domain: str, token: str) -> None: ...

    def clean_dns01(self, domain: str) -> None: ...
