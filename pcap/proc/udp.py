#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.util import BytesOrder, ProcData


class UDP(ProcData):
    """UDP 8B"""
    _src = 0
    _dst = 0
    # UDP头部和UDP数据的总长度字节
    _header_len = 0
    _check_sum = 0
    _data = None

    def __init__(self, data, upper):
        super(UDP, self).__init__(upper)
        self._src = data[:2]
        self._dst = data[2:4]
        self._header_len = data[4:6]
        self._check_sum = data[6:8]
        self._data = data[8:]

    def __str__(self):
        return "UDP src port:%d dst:%d header_len:%d check_sum:%s" % (
            self.src, self.dst, self.header_len, self.check_sum)

    @property
    def src(self):
        return BytesOrder.bytes2int(self._src, "big")

    @property
    def dst(self):
        return BytesOrder.bytes2int(self._dst, "big")

    @property
    def header_len(self):
        return BytesOrder.bytes2int(self._header_len, "big")

    @property
    def check_sum(self):
        return self._check_sum

    @property
    def data(self):
        return self._data
