# -*- coding: utf8 -*-

from abc import abstractmethod

class CadcUtils(object):
    @abstractmethod
    def split_domain_name(domain: str) -> list: ...
