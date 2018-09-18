#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.mac import MAC
from pcap.proc.util import BytesBuffer, BytesOrder, ProcData


class PacketHead(object):
    """包头 16B"""
    _ts_sec = 0
    _ts_usec = 0
    _incl_len = 0
    _orig_len = 0

    def __init__(self, data):
        self._ts_sec = BytesOrder.bytes2int(data[:4])
        self._ts_usec = BytesOrder.bytes2int(data[4:8])
        self._incl_len = BytesOrder.bytes2int(data[8:12])
        self._orig_len = BytesOrder.bytes2int(data[12:16])

    @property
    def sec(self):
        return self._ts_sec

    @property
    def usec(self):
        return self._ts_usec

    @property
    def incl(self):
        return self._incl_len

    @property
    def orig(self):
        return self._orig_len

    def __str__(self):
        return "PACKET sec:%d usec:%d incl len:%d orig len:%d" % (
            self._ts_sec, self._ts_usec, self._incl_len, self._incl_len)


class Packet(ProcData):
    """数据包(未拆包)"""
    _head = None
    _buff = None
    name = "Packet"

    def __init__(self):
        super(ProcData, self).__init__()
        self._buff = BytesBuffer()

    def parse(self, data):
        """
        解析包数据
        :param data: 字节数据
        :return:    data,size
        """
        size = len(data)
        assert size > 0
        if self._head is None:
            self._head = PacketHead(data)
            size -= 16
            data = data[16:]
        if size > 0:
            _bs = len(self._buff)
            if _bs + size < self._head.incl:
                self._buff.write(data)
                size = 0
                data = None
            else:
                offset = self._head.incl - _bs
                self._buff.write(data[:offset])
                data = data[offset:]
                size -= offset
                assert len(data) == size
        return data, size

    def __del__(self):
        self._buff.close()

    @property
    def head(self):
        return self._head

    @property
    def data(self):
        return MAC(self._buff.getvalue(),None)

    def finish(self):
        return len(self._buff) == self._head.incl
