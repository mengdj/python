#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from pcap.proc.tcp_build import OnlyId
from pcap.proc.util import AppProcData, BytesBuffer

RTMP_CLIENT = 0x00
RTMP_SERVER = 0x01
RTMP_VERSION = 0x03
RTMP_PORT = 1935


class RTMP_Chunk_Basic_Head(object):
    __fmt = 0
    __cs_id = 0


class RTMP_Chunk_Msg_Head(object):
    pass


class RTMP_Chunk_Timestamp(object):
    pass


class RTMP_Chunk_Data(object):
    pass


class RTMP_Chunk(object):
    def __init__(self, data):
        pass


class RTMP(AppProcData):
    """
        尝试rtmp协议解析,默认端口1935
        参考文档:https://www.cnblogs.com/android-blogs/p/5650771.html
    """
    c0 = None
    _c1 = None
    _c2 = None
    s0 = None
    _s1 = None
    _s2 = None
    _buff = None
    _chunk = None

    __prev_rtmp = {}
    __fn = None
    __ins = None

    def __init__(self):
        self._c1 = BytesBuffer()
        self._c2 = BytesBuffer()
        self._s1 = BytesBuffer()
        self._s2 = BytesBuffer()
        self._buff = BytesBuffer()

    def bind(self, fn):
        """
        绑定回调函数
        :param fn:  回调函数    callback_rtmp(ins, msg, fr)
        :return:
        """
        self.__fn = fn

    @property
    def info(self):
        pass

    def _process(self, data, fr=0):
        """
        解析thunk信息
        :param data:    元数据
        :param fr:      调用来源    RTMP_CLIENT|RTMP_SERVER
        :return:        None
        """
        if len(self._buff) > 0:
            self._buff.write(data)
            data = self._buff.getvalue()
            self._buff.clear()
        self._chunk = RTMP_Chunk(data)
        return self.__fn(self, self._chunk, fr)

    @staticmethod
    def find(tcp, fn):
        """
        校验数据并完成初始化，成功返回self，链式调用
        :param tcp:     上层调用者tcp对象
        :param fn:      回调函数
        :return:
        """
        assert fn is not None
        data = tcp.data
        size = len(data)
        if size > 0:
            # 4元祖确定连接
            only_id = OnlyId.build(tcp.upper.src, tcp.upper.dst, tcp.src, tcp.dst)
            if tcp.dst == RTMP_PORT:
                # client
                if only_id not in RTMP.__prev_rtmp:
                    # 每一个链路触发一个对象
                    ins = RTMP()
                    ins.bind(fn)
                    if data[0] == RTMP_VERSION:
                        ins.c0 = data[0]
                        ins.__fn(ins, "C0", RTMP_CLIENT)
                        data = data[1:]
                        size -= 1
                        # 剩下最大值mss也不够1536
                        if size > 0:
                            ins._c1.write(data)
                        RTMP.__prev_rtmp[only_id] = ins
                else:
                    tmp = RTMP.__prev_rtmp.get(only_id)
                    c1_size = len(tmp._c1)
                    if c1_size == 1536:
                        c2_size = len(tmp._c2)
                        if c2_size == 1536:
                            # 握手完成，处理数据
                            tmp._process(data, RTMP_CLIENT)
                        else:
                            last_c2size = 1536 - c2_size
                            tmp._c2.write(data[:last_c2size])
                            data = data[last_c2size:]
                            size -= last_c2size
                            if len(tmp._c2) == 1536:
                                # 写入c1
                                tmp.__fn(tmp, "C2", RTMP_CLIENT)
                            if last_c2size > 0:
                                # 写入c2
                                tmp._c2.write(data)
                    else:
                        last_c1size = 1536 - c1_size
                        tmp._c1.write(data[:last_c1size])
                        data = data[last_c1size:]
                        size -= last_c1size
                        if len(tmp._c1) == 1536:
                            # 写入c1
                            tmp.__fn(tmp, "C1", RTMP_CLIENT)
                        if size > 0:
                            # 写入c2
                            tmp._c2.write(data)
            elif tcp.src == RTMP_PORT:
                # server
                if only_id not in RTMP.__prev_rtmp:
                    if data[0] == RTMP_VERSION:
                        ins = RTMP()
                        ins.bind(fn)
                        ins.s0 = data[0]
                        ins.__fn(ins, "S0", RTMP_SERVER)
                        data = data[1:]
                        size -= 1
                        # 剩下最大值mss也不够1536,就不用判断了
                        if size > 0:
                            ins._s1.write(data)
                        RTMP.__prev_rtmp[only_id] = ins
                else:
                    tmp = RTMP.__prev_rtmp.get(only_id)
                    s1_size = len(tmp._s1)
                    if s1_size == 1536:
                        s2_size = len(tmp._s2)
                        if s2_size == 1536:
                            # 握手完成，处理数据
                            tmp._process(data, RTMP_SERVER)
                        else:
                            last_s2size = 1536 - s2_size
                            tmp._s2.write(data[:last_s2size])
                            data = data[last_s2size:]
                            size -= last_s2size
                            if len(tmp._s2) == 1536:
                                # 写入c1
                                tmp.__fn(tmp, "S2", RTMP_SERVER)
                            if last_s2size > 0:
                                # 写入c2
                                tmp._s2.write(data)
                    else:
                        last_s1size = 1536 - s1_size
                        tmp._s1.write(data[:last_s1size])
                        data = data[last_s1size:]
                        size -= last_s1size
                        if len(tmp._s1) == 1536:
                            # 写入s1
                            tmp.__fn(tmp, "S1", RTMP_SERVER)
                        if size > 0:
                            # 写入s2
                            tmp._s2.write(data)
            else:
                return False
        return True
