# -*- coding: utf8 -*-

from abc import abstractmethod


class CadcUtils(object):
    @staticmethod
    def split_domain_name(domain):
        """
        Split domian name into sub domain and main domain pairs.
        main domain contains at least one dot character.
        Shortest main domain is in low index of returned list.
        
        :param domain: a domain name . such as 'aaa.test12.kingsilk.com.cn'
        :return:  [(sub_domain,main_domain),(sub_domain,main_domain),...] 
        """
        assert domain and type(domain) == str, "argument `domain` is required."

        assert type(domain) == str, "Expected argument `domain` is str."
        assert domain.find(".") >= 0, "`domain` doest not contain dot character."
        l = domain.split(".")
        results = []
        for i in range(len(l) - 1):
            sub_domain = ".".join(l[0:i])
            main_domain = ".".join(l[i:])
            results.append((sub_domain, main_domain))

        results.reverse()

        return results
