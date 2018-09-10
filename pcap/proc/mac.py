#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from proc.arp import ARP
from proc.ip import IP
from proc.ipv6 import IPV6
from proc.util import ProcData


class MAC(ProcData):
    """mac协议 14B+"""
    _dst = None
    _src = None
    _type = None
    _data = None

    def __init__(self, data):
        super(ProcData, self).__init__()
        size = len(data)
        assert size > 18
        self._dst = data[:6]
        self._src = data[6:12]
        self._type = data[12:14]
        # fcs校验字段 self._fcs = data[size - 4:]
        self._data = data[14:]

    def __str__(self):
        return "dst=>%s src=>%s type:%s" % (self.dst, self.src, self.type)

    @property
    def dst(self):
        return [hex(s).replace("0x", "").upper() for s in self._dst]

    @property
    def src(self):
        return [hex(s).replace("0x", "").upper() for s in self._src]

    @property
    def type(self):
        return [hex(i) for i in self._type]

    @property
    def data(self):
        ret = None
        if self._type[0] == 0x08:
            if self._type[1] == 0x00:
                # ipv4 0x0800
                ret = IP(self._data)
            elif self._type[1] == 0x06:
                # arp 0x0806
                ret = ARP(self._data)
        elif self._type[0] == 0x86:
            if self._type[1] == 0xdd:
                # ipv6 0x86dd
                ret = IPV6(self._data)
        return ret
