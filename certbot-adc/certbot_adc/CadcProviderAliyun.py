# -*- coding: utf8 -*-

from CadcProviderBase import CadcProviderBase
import json
import logging

from aliyunsdkalidns.request.v20150109 import \
    AddDomainRecordRequest, \
    UpdateDomainRecordRequest, \
    DescribeDomainRecordsRequest, \
    DescribeDomainRecordInfoRequest, \
    DeleteDomainRecordRequest, \
    DescribeDomainInfoRequest

from aliyunsdkcore.acs_exception.exceptions import ServerException

logger = logging.getLogger("certbot_adc.CadcProviderAliyun")


class CadcProviderAliyun(CadcProviderBase):
    acs_client = None

    def __init__(self, acs_client):
        self.acs_client = acs_client

    def get_owned_domain_info(self, main_domain):

        req = DescribeDomainInfoRequest.DescribeDomainInfoRequest()
        req.set_DomainName(main_domain)

        try:
            resp_str = self.acs_client.do_action_with_exception(req)
            logger.debug("owns_domain:" + resp_str)
            resp_dict = json.loads(resp_str)
            return resp_dict
        except ServerException as e:
            logger.debug("owns_domain: not owns domain '" + main_domain + "'" + str(e))

        return None

    def owns_domain(self, full_domain):

        # check root matches
        # aaa.test.kingsilk.net.cn
        #                -> net.cn
        #       -> kingsilk.net.cn
        #  -> test.kingsilk.net.cn

        i = full_domain.rfind(".")
        if i == -1:
            return None

        i = full_domain.rfind(".", 0, i)

        # full_domain is like "kingsilk.xyz"
        if i == -1:
            domain_info_dict = self.get_owned_domain_info(full_domain)

            if domain_info_dict and domain_info_dict.get("DomainId"):
                return ("", full_domain)

        # full_domain is like "test12.kingsilk.xyz"
        while i >= 0:
            r = full_domain[i + 1:]

            domain_info_dict = self.get_owned_domain_info(r)

            if domain_info_dict and domain_info_dict.get("DomainId"):
                sp_idx = full_domain.rfind(r)
                sub_domain = full_domain[0:sp_idx - 1]
                return (sub_domain, r)

            i = full_domain.find(".", 0, i)

        return None

    def get_txt_record(self, record_id):

        req = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
        req.set_RecordId(record_id)

        resp_str = self.acs_client.do_action_with_exception(req)
        resp_dict = json.loads(resp_str)

        logger.debug("get_txt_record:" + resp_str)

        return resp_dict

    def update_txt_record(self, record_id, rr, value):

        req = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        req.set_RecordId(record_id)
        req.set_Type("TXT")
        req.set_RR(rr)
        req.set_Value(value)

        resp_str = self.acs_client.do_action_with_exception(req)
        resp_dict = json.loads(resp_str)

        logger.debug("update_txt_record:" + resp_str)

        record_id = resp_dict.get('RecordId')
        if record_id and type(record_id) == str:
            return record_id
        else:
            return None

    def delete_txt_record(self, record_id):

        req = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
        req.set_RecordId(record_id)

        try:
            resp_str = self.acs_client.do_action_with_exception(req)
            logger.debug("delete_txt_record:" + resp_str)
        except ServerException as e:
            logger.warning("delete_txt_record: could not delete DNS TXT record " + str(e))
            pass

    def add_txt_record(self, domain, rr, value):

        req = AddDomainRecordRequest.AddDomainRecordRequest()
        req.set_DomainName(domain)
        req.set_Type("TXT")
        req.set_RR(rr)
        req.set_Value(value)

        resp_str = self.acs_client.do_action_with_exception(req)
        resp_dict = json.loads(resp_str)
        record_id = resp_dict.get('RecordId')

        logger.debug("add_txt_record:" + resp_str)

        if record_id and type(record_id) == str:
            return record_id
        else:
            return None

    def find_target_txt_record(self, domain, rr):
        req = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        # req.set_accept_format("JSON")
        req.set_DomainName(domain)
        req.set_PageNumber(1)
        req.set_PageSize(500)
        req.set_RRKeyWord(rr)

        resp_str = self.acs_client.do_action_with_exception(req)
        resp_dict = json.loads(resp_str)

        logger.debug("find_target_txt_record:" + resp_str)

        total_count = resp_dict.get("TotalCount")

        if total_count and type(total_count) == int:

            for rec in resp_dict["DomainRecords"]["Record"]:
                if rec["Type"] == 'TXT' and rec['RR'] == rr:
                    return rec['RecordId']

        return None

    def update_dns01(self, domain, token):

        # domain =            'kingsilk.com'
        # domain =     'test12.kingsilk.xyz'
        # domain = 'aaa.test12.kingsilk.xyz'
        d = self.owns_domain(domain)

        assert d, "Not owned domain '" + domain + "'"
        sub_domain, main_domain = d

        if sub_domain:
            sub_domain = sub_domain.rstrip(".")

        if sub_domain:
            sub_domain = "_acme-challenge." + sub_domain
        else:
            sub_domain = "_acme-challenge"

        record_id = self.find_target_txt_record(main_domain, sub_domain)

        if record_id:
            rec_resp = self.get_txt_record(record_id)

            if rec_resp is not None and type(rec_resp) == dict and rec_resp.get('Value') != token:
                self.update_txt_record(record_id, sub_domain, token)
                logger.info("Updating existed DNS TXT record.")
            else:
                logger.error("Same token already been configured. Skip.")
        else:
            self.add_txt_record(main_domain, sub_domain, token)
            logger.info("DNS TXT record added.")

    def clean_dns01(self, domain):
        d = self.owns_domain(domain)

        assert d, "Not owned domain '" + domain + "'"
        sub_domain, main_domain = d

        if sub_domain:
            sub_domain = sub_domain.rstrip(".")

        if sub_domain:
            sub_domain = "_acme-challenge." + sub_domain
        else:
            sub_domain = "_acme-challenge"

        record_id = self.find_target_txt_record(main_domain, sub_domain)

        if record_id:
            self.delete_txt_record(record_id)
