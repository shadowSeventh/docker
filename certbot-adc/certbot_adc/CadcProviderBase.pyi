# -*- coding: utf8 -*-

from abc import abstractmethod


class CadcProviderBase:
    @abstractmethod
    def update_dns01(self, domain: str, token: str) -> None: ...

    @abstractmethod
    def clean_dns01(self, domain: str) -> None: ...
