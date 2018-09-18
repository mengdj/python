#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.util import BytesOrder, ProcData


class Flag(object):
    """
　　 CWR：拥塞窗口减少标志被发送主机设置，用来表明它接收到了设置ECE标志的TCP包。拥塞窗口是被TCP维护
         的一个内部变量，用来管理发送窗口大小。
    ECE：ECN响应标志被用来在TCP3次握手时表明一个TCP端是具备ECN功能的，并且表明接收到的TCP包的IP
         头部的ECN被设置为11。更多信息请参考RFC793。
    URG：紧急标志。紧急标志为"1"表明该位有效。
    ACK：确认标志。表明确认编号栏有效。大多数情况下该标志位是置位的。TCP报头内的确认编号栏内包含的
         确认编号（w+1）为下一个预期的序列编号，同时提示远端系统已经成功接收所有数据。
    PSH：推标志。该标志置位时，接收端不将该数据进行队列处理，而是尽可能快地将数据转由应用处理。在处理
         Telnet或rlogin等交互模式的连接时，该标志总是置位的。
    RST：复位标志。用于复位相应的TCP连接。
    SYN：同步标志。表明同步序列编号栏有效。该标志仅在三次握手建立TCP连接时有效。它提示TCP连接的服务端
         检查序列编号，该序列编号为TCP连接初始端（一般是客户端）的初始序列编号。在这里，可以把TCP序列
         编号看作是一个范围从0到4，294，967，295的32位计数器。通过TCP连接交换的数据中每一个字节都经
         过序列编号。在TCP报头中的序列编号栏包括了TCP分段中第一个字节的序列编号。
    FIN：结束标志。
    """
    CWR = 0
    ECE = 0
    URG = 0
    ACK = 0
    PSH = 0
    RST = 0
    SYN = 0
    FIN = 0

    def __init__(self, flag):
        # 取反补位(一次1字节的后6位)
        self.CWR = ((~(~(1 << 7))) & flag) >> 7
        self.ECE = ((~(~(1 << 6))) & flag) >> 6
        self.URG = ((~(~(1 << 5))) & flag) >> 5
        self.ACK = ((~(~(1 << 4))) & flag) >> 4
        self.PSH = ((~(~(1 << 3))) & flag) >> 3
        self.RST = ((~(~(1 << 2))) & flag) >> 2
        self.SYN = ((~(~(1 << 1))) & flag) >> 1
        self.FIN = ((~(~1)) & flag)

    def __str__(self):
        return "(CWR:%d ECE:%d URG:%d ACK:%d PSH:%d RST:%d SYN:%d FIN:%d)" % (
            self.CWR, self.ECE, self.URG, self.ACK, self.PSH, self.RST, self.SYN, self.FIN)


class TCP(ProcData):
    """UDP协议 20B+，暂未处理分段数据 """
    _src = 0
    _dst = 0
    # 发送、确认编号
    _seq_no = 0
    _ack_no = 0
    _header_len_reserved = 0
    _reserved_flag = 0
    _wnd_size = 0
    _check_sum = 0
    # 紧急指针(偏移量)
    _urqt_p = 0
    _option = []
    _flag = None
    _data = []

    def __init__(self, data, upper):
        super(TCP, self).__init__(upper)
        self._src = data[:2]
        self._dst = data[2:4]
        self._seq_no = data[4:8]
        self._ack_no = data[8:12]
        # 4+4
        self._header_len_reserved = data[12]
        # 2+6
        self._reserved_flag = data[13]
        self._wnd_size = data[14:16]
        self._check_sum = data[16:18]
        self._urqt_p = data[18:20]
        # 其他可选字段
        if self.header_len > 20:
            self._option = data[20:self.header_len]
        self._data = data[self.header_len:]

    def __str__(self):
        return "TCP src(port):%d dst(port):%d seq:%d ack:%d len(header):%d " \
               "flag:%s win:%d check_sum:%s urqt_p:%d option:%d payload:%d" % (
                   self.src, self.dst, self.seq, self.ack, self.header_len, self.flag, self.wnd_size,
                   self.check_sum, self.urqt_p,
                   len(self._option),
                   len(self._data))

    def __len__(self):
        return len(self._data)

    @property
    def src(self):
        return BytesOrder.bytes2int(self._src, "big")

    @property
    def option(self):
        """分析tcp的可选项字段(分析了常用字段)"""
        size = len(self._option)
        ret = []
        if size > 0:
            option = self._option
            while size > 0:
                if option[0] == 0x00:
                    ret.append({"END": option[0]})
                    break
                if option[0] == 0x01:
                    ret.append({"NOP": option[0]})
                    size -= 1
                    option = option[1:]
                elif option[0] == 0x02:
                    # MSS
                    ret.append({"MSS": {"length": option[1], "value": BytesOrder.bytes2int(option[2:4], "big")}})
                    size -= 4
                    option = option[4:]
                elif option[0] == 0x03:
                    # 窗口扩大因子
                    ret.append({"WSALE": {"length": option[1], "shift_count": option[2]}})
                    size -= 3
                    option = option[3:]
                elif option[0] == 0x04:
                    # SACK
                    ret.append({"SACK": {"length": option[1]}})
                    size -= 2
                    option = option[2:]
                elif option[0] == 0x08:
                    # 时间戳
                    ret.append({"TIMESTAMP": {"length": option[1], "value": BytesOrder.bytes2int(option[2:6], "big"),
                                              "repl_value": BytesOrder.bytes2int(option[6:10], "big")}})
                    size -= 10
                    option = option[10:]
                else:
                    break
        else:
            ret = None
        return ret

    @property
    def flag(self):
        """获取标志对象"""
        if self._flag is None:
            self._flag = Flag(self._reserved_flag)
        return self._flag

    @property
    def flag_desc(self):
        return bin(self._reserved_flag)

    @property
    def dst(self):
        return BytesOrder.bytes2int(self._dst, "big")

    @property
    def seq(self):
        """获取序列号"""
        return BytesOrder.bytes2int(self._seq_no, "big")

    @property
    def ack(self):
        """获取确认号"""
        return BytesOrder.bytes2int(self._ack_no, "big")

    @property
    def header_len(self):
        """获取头部长度"""
        return (self._header_len_reserved >> 4) << 2

    @property
    def wnd_size(self):
        """获取滑动窗口大小"""
        return BytesOrder.bytes2int(self._wnd_size, "big")

    @property
    def check_sum(self):
        """获取校验"""
        return self._check_sum

    @property
    def urqt_p(self):
        """获取紧急指针"""
        return BytesOrder.bytes2int(self._urqt_p, "big")

    @property
    def data(self):
        """获取原始包(可能包含分段数据，此数据未进行重组)"""
        return self._data
