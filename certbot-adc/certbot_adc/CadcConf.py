# -*- coding: utf8 -*-


import yaml
from validate_email import validate_email
import os
import logging
from certbot_adc.CadcUtils import CadcUtils

logger = logging.getLogger("certbot_adc.CadcConf")


class CadcConf:
    """
    key     : domainName        # str
    value   : ...               # dict, == `providers[?]`
    """
    domain_mappings = {}
    name_mappings = {}
    conf_file = None

    def __init__(self, conf_file=None):

        if conf_file:
            assert os.path.isfile(conf_file), \
                "config file '" + conf_file + "' is not existed."
            self.conf_file = conf_file
        else:
            self.conf_file = self.find_conf_file()

        self.check()

    def find_conf_file(self):
        configs = [
            os.environ.get("CERTBOT_ADC_YAML"),
            os.getcwd() + os.sep + "certbot_adc.yaml",
            os.getcwd() + os.sep + "config" + os.sep + "certbot_adc.yaml",
            os.path.expanduser("~") + os.sep + ".certbot_cadc" + os.sep + "certbot_adc.yaml",
            os.sep + "etc" + os.sep + "certbot_adc" + os.sep + "certbot_adc.yaml"
        ]
        config = None
        for config_file in configs:
            if config_file and os.path.isfile(config_file):
                config = config_file
                break

        assert config, """
        Could not find certbot_adc.yaml in  
        1. Environment variable 'CERTBOT_ADC_YAML'
        2. $WORKING_DIR/certbot_adc.yaml
        3. $WORKING_DIR/config/certbot_adc.yaml
        4. ~/.certbot_cadc/certbot_adc.yaml
        5. /etc/certbot_cadc/certbot_adc.yaml
        """
        logger.info("Using config file '" + config + "'")
        return config

    def check_provider_aliyun(self, name, provider):
        key_id = provider.get("keyId")
        assert key_id and type(key_id) == str, \
            "`providers '" + name + "' : `keyId` is not configured correctly in yaml file."

        key_secret = provider.get("keySecret")
        assert key_secret and type(key_secret) == str, \
            "`providers '" + name + "' : `keySecret` is not configured correctly in yaml file."

        region = provider.get("region")
        assert region and type(region) == str, \
            "`providers '" + name + "' : `region` is not configured correctly in yaml file."

        domains = provider.get("domains")
        assert domains and type(domains) == list, \
            "`providers '" + name + "' : `domains` is required as list."

        for domain in provider["domains"]:
            assert domain and type(domain) == str, \
                "`providers '" + name + "' : `domains` require non empty strings."

    def check_provider_qcloud(self, name, provider):
        self.check_provider_aliyun(name, provider)

    def map_by_domain(self):
        for name, provider in self.name_mappings.items():
            for domain in provider["domains"]:
                assert domain and type(domain) == str, \
                    "`providers '" + name + "' : `domains` require non empty strings."

                existed_provider = self.domain_mappings.get(domain)

                if existed_provider is not None:
                    assert False, \
                        "`domain '" + domain + "' is configured both in provider '" \
                        + existed_provider['name'] + "' and '" + provider['name'] + "'."

                self.domain_mappings[domain] = provider

    def find_provider_by_domain(self, domain):

        # full match ("aaa.test.kingsilk.net.cn" eg.)
        l = list(reversed(CadcUtils.split_domain_name(domain)))

        for sub_domain, main_domain in l:

            m = self.domain_mappings.get(main_domain)
            if m:
                return m

        return None

    def check(self):
        conf_dict = yaml.load(open(self.conf_file, "r").read())

        providers = conf_dict.get("providers")
        assert providers is not None and type(providers) == dict, \
            "`providers` is not configured correctly in yaml file."

        self.name_mappings = providers

        for name, provider in providers.items():

            _type = provider.get("type")
            provider["name"] = name

            if _type == 'aliyun':
                self.check_provider_aliyun(name, provider)
            elif _type == 'qcloud':
                self.check_provider_qcloud(name, provider)
            else:
                assert False, \
                    "`providers '" + name + "' : `type` is not supported."

        self.map_by_domain()
