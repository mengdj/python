#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.tcp import TCP
from pcap.proc.udp import UDP
from pcap.proc.util import BytesOrder, ProcData


class Services(object):
    """IP服务类型"""
    PRIORITY = 0
    DELAY = 0
    THROUGHPUT = 0
    RELIABILITY = 0
    COST = 0
    RESERVED = 0

    def __init__(self, ser):
        pass


class Flag(object):
    """IP分片标志(python偏移真坑)"""
    DF = 0
    MF = 0

    def __init__(self, flag):
        """
            如果DF=0，那么标识不允许分段；DF=1则是表示这个数据包允许分段。MF=0表示分完段
            之后这个数据段是整个包的最后那段，MF=1则是不是最后段的标志
        """
        self.DF = ((~(~(1 << 6))) & flag) >> 6
        self.MF = ((~(~(1 << 5))) & flag) >> 5

    def __str__(self):
        return "(DF:%d MF:%d)" % (self.DF, self.MF)


class IP(ProcData):
    """ip协议(ipv4) 20B"""
    _header_version_len = 0
    _service_set = 0
    # 标示IP头部有多少个4字节，IP头部最长是60字节
    _total_len = 0
    _id = 0
    _flag_offset = 0
    _time_to_live = 0
    _protocol = 0
    _check_sum = 0
    _src = 0
    _dst = 0
    _data = None
    _flag = None

    def __init__(self, data, upper):
        super(IP, self).__init__(upper)
        # 版本和长度各占4位，一共1个字节
        self._header_version_len = data[0]
        self._service_set = data[1]
        self._total_len = data[2:4]
        self._id = data[4:6]
        self._flag_offset = data[6:8]
        self._time_to_live = data[8]
        self._protocol = data[9]
        self._check_sum = data[10:12]
        self._src = data[12:16]
        self._dst = data[16:20]
        self._data = data[self.head_len_byte:]

    def __str__(self):
        return (
                "IPv%d src:%s dst:%s len(header):%d service:%s len(total):%d id:%d flag:%s "
                "time to live:%d protocol:%d check sum:%s payload:%d" %
                (
                    self.version, self.src, self.dst, self.head_len_byte, bin(self._service_set), self.total_len,
                    self.id,
                    self.flag, self.time_to_live, self._protocol,
                    self._check_sum, len(self._data))
        )

    @property
    def version(self):
        return self._header_version_len >> 4

    @property
    def head_len(self):
        return (0xff >> 4) & self._header_version_len

    @property
    def flag(self):
        if self._flag is None:
            self._flag = Flag(self._flag_offset[0])
        return self._flag

    @property
    def total_len(self):
        return BytesOrder.bytes2int(self._total_len, "big")

    @property
    def time_to_live(self):
        return self._time_to_live

    @property
    def id(self):
        """IP序号"""
        return BytesOrder.bytes2int(self._id, "big")

    @property
    def src(self):
        return [i for i in self._src]

    @property
    def dst(self):
        return [i for i in self._dst]

    @property
    def head_len_byte(self):
        """头部字节数"""
        return self.head_len << 2

    @property
    def data(self):
        """获取传输层协议"""
        ret = None
        # 46~1500 检测是否有填充数据(既数据部分不满足46字节会填充，传递时候要过滤掉这部分数据)
        # tcp自身有分包机制，不用处理分包，其他协议需要处理分包
        data = self._data[:self.total_len - 20]
        if self._protocol == 0x06:
            ret = TCP(data, self)
        elif self._protocol == 0x11:
            ret = UDP(data, self)
        return ret
