#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.arp import ARP
from pcap.proc.ip import IP
from pcap.proc.ipv6 import IPV6
from pcap.proc.util import ProcData


class MAC(ProcData):
    """mac协议 14B+"""
    _dst = None
    _src = None
    _type = None
    _data = None

    def __init__(self, data, upper):
        super(MAC, self).__init__(upper)
        size = len(data)
        assert size > 18
        self._dst = data[:6]
        self._src = data[6:12]
        self._type = data[12:14]
        # fcs校验字段 self._fcs = data[size - 4:]
        self._data = data[14:]

    def __str__(self):
        return "MAC dst=>%s src=>%s type:%s" % (self.dst_desc, self.src_desc, self.type_desc)

    @property
    def dst_desc(self):
        return [hex(s).replace("0x", "").upper() for s in self._dst]

    @property
    def src_desc(self):
        return [hex(s).replace("0x", "").upper() for s in self._src]

    @property
    def type_desc(self):
        return [hex(i) for i in self._type]

    @property
    def dst(self):
        return self._dst

    @property
    def src(self):
        return self._src

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        ret = None
        if self._type[0] == 0x08:
            if self._type[1] == 0x00:
                # ipv4 0x0800
                ret = IP(self._data, self)
            elif self._type[1] == 0x06:
                # arp 0x0806
                ret = ARP(self._data, self)
        elif self._type[0] == 0x86:
            if self._type[1] == 0xdd:
                # ipv6 0x86dd
                ret = IPV6(self._data, self)
        return ret
