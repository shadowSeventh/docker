# -*- coding: utf8 -*-

import json
import logging
from CadcProviderBase import CadcProviderBase
from CadcUtils import CadcUtils

logger = logging.getLogger("certbot_adc.CadcProviderQcloud")


class CadcProviderQcloud(CadcProviderBase):
    api = None

    def __init__(self, qcloud_api):
        self.api = qcloud_api

    def update_txt_record(self, main_domain, record_id, sub_domain, value):
        resp_str = self.api.call("RecordModify", {
            "domain": main_domain,
            "recordId": record_id,
            "subDomain": sub_domain,
            "recordType": "TXT",
            "recordLine": "默认",
            "value": value

        })
        logger.debug("update_txt_record:" + resp_str)

        resp_dict = json.loads(resp_str)
        assert resp_dict and resp_dict.get("code") == 0, \
            "Faild to update DNS TXT record."

    def add_txt_record(self, main_domain, sub_domain, value):
        resp_str = self.api.call("RecordCreate", {
            "domain": main_domain,
            "subDomain": sub_domain,
            "recordType": "TXT",
            "recordLine": "默认",
            "value": value

        })
        resp_dict = json.loads(resp_str)
        logger.debug("add_txt_record:" + resp_str)

        assert resp_dict and resp_dict.get("code") == 0, \
            "Faild to add DNS TXT record."

    def get_txt_record(self, main_domain, sub_domain):

        """
        check whether the TXT record is existed.
        :return: 
        """

        # get DNS record list, should return zeor or only one record.

        records_str = self.api.call("RecordList", {
            "domain": main_domain,
            "offset": 0,
            "length": 100,
            "subDomain": sub_domain,
            "recordType": "TXT"
        })
        logger.debug("get_txt_record:" + records_str)

        records_dict = json.loads(records_str)
        assert records_dict and records_dict.get("code") == 0, \
            "Faild get domain record list, response is : " + records_str

        record_total = int(records_dict["data"]["info"]["record_total"])
        assert record_total <= 1, \
            "Argument sub_domain = '" + sub_domain + "' main_domain = '" + main_domain + \
            "'matches more than one records. response : " + records_str

        if record_total == 1:
            rec = records_dict["data"]["records"][0]
            return (
                rec["id"],
                rec["value"]
            )

        return None

    def delete_txt_record(self, main_domain, record_id):

        resp_str = self.api.call("RecordDelete", {
            "domain": main_domain,
            "recordId": record_id
        })
        resp_dict = json.loads(resp_str)
        logger.debug("delete_txt_record:" + resp_str)

        assert resp_dict and resp_dict.get("code") == 0, \
            "Faild to delete DNS TXT record."

    def owns_domain(self, domain):
        """
        check whether owns the domain, and split into sub_domain, and main_domain.
        :param domain: full domain string
        :return:  two elements tuple which contains sub_domain and main_domain if owns
                  or None if not owns
        """

        pairs = CadcUtils.split_domain_name(domain)

        # get owns domain list

        next_offset = 0
        page_size = 100
        domain_total = -1

        while True:
            domains_str = self.api.call("DomainList", {
                "offset": next_offset,
                "length": page_size
            })
            logger.debug("owns_domain:" + domains_str)

            domains_dict = json.loads(domains_str)
            assert domains_dict and domains_dict.get("code") == 0, \
                "Faild get domain list, response is : " + domains_str

            for sub_domain, main_domain in pairs:
                for d in domains_dict["data"]["domains"]:
                    if d["name"] == main_domain:
                        return (sub_domain, main_domain)

            # has next page ?
            next_offset = next_offset + page_size

            if domain_total < 0:
                domain_total = domains_dict["data"]["info"]["domain_total"]

            if next_offset >= domain_total:
                break

        return None

    def update_dns01(self, domain, token):
        pair = self.owns_domain(domain)

        assert pair, "Not owns the domain `" + domain + "`."

        sub_domain, main_domain = pair

        if sub_domain:
            sub_domain = "_acme-challenge." + sub_domain
        else:
            sub_domain = "_acme-challenge"

        # DNS record already exists ?
        rec = self.get_txt_record(main_domain, sub_domain)

        if rec:
            record_id, record_value = rec

            if record_value != token:
                self.update_txt_record(main_domain, record_id, sub_domain, token)
                logger.info("Updating existed DNS TXT record.")
            else:
                logger.error("Same token already been configured. Skip.")
        else:
            self.add_txt_record(main_domain, sub_domain, token)
            logger.info("DNS TXT record added.")

    def clean_dns01(self, domain):
        pair = self.owns_domain(domain)

        assert pair, "Not owned domain '" + domain + "'"

        sub_domain, main_domain = pair

        if sub_domain:
            sub_domain = "_acme-challenge." + sub_domain
        else:
            sub_domain = "_acme-challenge"

        rec = self.get_txt_record(main_domain, sub_domain)

        if rec:
            self.delete_txt_record(main_domain, rec[0])
        pass
