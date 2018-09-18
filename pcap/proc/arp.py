#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.util import BytesOrder, ProcData


class ARP(ProcData):
    """ARP协议 24B or 28B"""
    _hardware = 0
    _protocol = 0
    _hardware_len = 0
    _protocol_len = 0
    # 1请求 2回复
    _operate = 0
    _src_mac = 0
    _src_ip = 0
    _dst_mac = 0
    _dst_ip = 0
    _crc = None
    _data = []

    def __init__(self, data, upper):
        super(ARP, self).__init__(upper)
        self._hardware = data[0:2]
        self._protocol = data[2:4]
        self._hardware_len = data[4]
        self._protocol_len = data[5]
        self._operate = data[6:8]
        self._src_mac = data[8:14]
        self._src_ip = data[14:18]
        self._dst_mac = data[18:24]
        self._dst_ip = data[24:28]
        self._data = data[28:]

    def __str__(self):
        return "ARP hardware:%s protocol:%s hardware_len:%d " \
               "protocol_len:%d operate:%d src:%s src_mac:%s dst:%s dst_mac:%s" % (
                   self.hardware, self.protocol, self.hardware_len, self.protocol_len, self.operate, self.src_ip,
                   self.src_mac,
                   self.dst_ip, self.dst_mac)

    @property
    def hardware(self):
        return self._hardware,

    @property
    def protocol(self):
        return self._protocol

    @property
    def hardware_len(self):
        return self._hardware_len

    @property
    def protocol_len(self):
        return self._protocol_len

    @property
    def src_ip(self):
        return [i for i in self._src_ip]

    @property
    def dst_ip(self):
        return [i for i in self._dst_ip]

    @property
    def src_mac(self):
        return [hex(s).replace("0x", "").upper() for s in self._src_mac]

    @property
    def dst_mac(self):
        return [hex(s).replace("0x", "").upper() for s in self._dst_mac]

    @property
    def operate(self):
        return BytesOrder.bytes2int(self._operate, "big")

    @property
    def data(self):
        return self._data
