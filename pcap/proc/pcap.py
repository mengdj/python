#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.packet import Packet
from pcap.proc.util import BytesBuffer
from pcap.proc.util import BytesOrder


class PcapHead(object):
    """pcap文件头 24B"""
    _magic_number = None
    _version_major = None
    _version_minor = None
    _thiszone = None
    _sigfigs = None
    _snaplen = None
    _link_type = None

    def __init__(self, data):
        assert len(data) == 24
        self._magic_number = data[:4]
        if PcapHead.signature(self._magic_number) is False:
            raise Exception("不支持的文件格式")
        self._version_major = BytesOrder.bytes2int(data[4:6])
        self._version_minor = BytesOrder.bytes2int(data[6:8])
        self._thiszone = BytesOrder.bytes2int(data[8:12])
        self._sigfigs = BytesOrder.bytes2int(data[12:16])
        self._snaplen = BytesOrder.bytes2int(data[16:20])
        self._link_type = BytesOrder.bytes2int(data[20:24])

    def __str__(self):
        return "order:%s magor:%d minor:%d zone:%d sig:%d snap_len:%d type:%d" % (
            BytesOrder.order, self._version_major, self._version_minor, self._thiszone, self._sigfigs, self._snaplen,
            self._link_type)

    @staticmethod
    def signature(data):
        """验证签名同时确定排序,虽然还无法读取到大小端但不影响"""
        sig = BytesOrder.bytes2int(data)
        if sig == 0xa1b2c3d4:
            BytesOrder.order = "big"
            return True
        elif sig == 0xd4c3b2a1:
            BytesOrder.order = "little"
            return True
        return False


class Pcap(object):
    """.pcap解析类"""
    __head = None
    __ret = 0

    def parse(self, file, buffSize=2048):
        """
        解析pcap文件,返回值为一个生成器 yield
        :param file:缓冲文件大小
        :param buffSize:
        :return:返回一个生成器（用于处理大包）
        """
        assert file != ""
        _buff = BytesBuffer()
        _packet = None
        ret = 0
        with open(file, "rb") as o:
            ctx = None
            while 1:
                # 优先处理缓冲区数据(如果缓存数据超过了指定大小)
                bsize = len(_buff)
                if bsize > 0:
                    if bsize >= buffSize:
                        ctx = _buff.getvalue()
                    else:
                        _buff.write(o.read(buffSize))
                        ctx = _buff.getvalue()
                    _buff.clear()
                else:
                    ctx = o.read(buffSize)
                size = len(ctx)
                if size > 0:
                    if self.__head is None:
                        # 文件头占24字节
                        if size >= 24:
                            self.__head = PcapHead(ctx[:24])
                            size -= 24
                            ctx = ctx[24:]
                        else:
                            _buff.write(ctx)
                    # 分析包头(包头占16字节)
                    if size > 16:
                        if _packet is None:
                            _packet = Packet()
                            ctx, size = _packet.parse(ctx)
                            if _packet.finish():
                                yield _packet
                                ret += 1
                                _packet = None
                            if size > 0:
                                _buff.write(ctx)
                        else:
                            ctx, size = _packet.parse(ctx)
                            if _packet.finish():
                                yield _packet
                                ret += 1
                                _packet = None
                            if size > 0:
                                _buff.write(ctx)
                    else:
                        _buff.write(ctx)
                else:
                    break
            del ctx
        del _buff
        self.__ret = ret

    def __len__(self):
        return self.__ret

    @property
    def head(self):
        """获取包头,务必保证有调用parse后才能获得包头"""
        return self.__head
